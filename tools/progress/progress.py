#!/usr/bin/env python3
"""UFQ progress tracker.

One dataset in (docs/progress/data/*.json), five views out: the Markdown hub,
roadmap, requirement register, guardrail board, decision ledger, plus a
standalone HTML dashboard.

Usage:
    python3 tools/progress/progress.py build          # regenerate every view
    python3 tools/progress/progress.py validate       # data integrity only
    python3 tools/progress/progress.py check          # validate + fail if views are stale
    python3 tools/progress/progress.py cite-check ... # every cited ID must exist
    python3 tools/progress/progress.py pr-report ...  # body for the PR bot comment
    python3 tools/progress/progress.py html --fragment  # artifact-ready HTML on stdout

Standard library only, by design: this must run before the stack decision
(ADR-0001) exists and on any machine a contributor happens to have.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs" / "progress" / "data"
OUT = ROOT / "docs" / "progress"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_html  # noqa: E402

BANNER = (
    "<!-- GENERATED FILE - do not edit by hand.\n"
    "     Source: docs/progress/data/*.json\n"
    "     Regenerate: python3 tools/progress/progress.py build -->\n"
)

# --------------------------------------------------------------------------
# vocabulary
# --------------------------------------------------------------------------

# weight None = excluded from percentage maths (not a commitment yet)
DELIVERY_STATUS = {
    "not-started":  {"label": "Not started",  "icon": "\u2b1c", "tone": "idle",     "weight": 0.0},
    "in-progress":  {"label": "In progress",  "icon": "\U0001f7e1", "tone": "active", "weight": 0.5},
    "shipped":      {"label": "Shipped",      "icon": "\U0001f7e2", "tone": "done",  "weight": 1.0},
    "verified":     {"label": "Verified",     "icon": "\u2705", "tone": "done",     "weight": 1.0},
    "blocked":      {"label": "Blocked",      "icon": "\u26d4", "tone": "bad",      "weight": 0.0},
    "deferred":     {"label": "Deferred",     "icon": "\U0001f4a4", "tone": "muted", "weight": None},
    "concept":      {"label": "Concept",      "icon": "\U0001f4d0", "tone": "muted", "weight": None},
}

COMPLIANCE_STATUS = {
    "upheld":          {"label": "Upheld",          "icon": "\U0001f6e1\ufe0f", "tone": "done"},
    "at-risk":         {"label": "At risk",         "icon": "\u26a0\ufe0f", "tone": "warn"},
    "violated":        {"label": "Violated",        "icon": "\U0001f6a8", "tone": "bad"},
    "not-applicable":  {"label": "Nothing to check yet", "icon": "\u2796", "tone": "idle"},
    "not-yet-binding": {"label": "Not yet binding", "icon": "\U0001f4d0", "tone": "muted"},
}

CONTEXT_STATUS = {"reference": {"label": "Reference", "icon": "\U0001f4d6", "tone": "muted"}}

TRACK_VOCAB = {
    "delivery": DELIVERY_STATUS,
    "compliance": COMPLIANCE_STATUS,
    "context": CONTEXT_STATUS,
}

KIND_LABEL = {
    "ground-truth": "Ground truths",
    "principle": "Design principles",
    "role": "Users and roles",
    "module": "Modules",
    "feature": "Functional requirements",
    "nfr": "Non-functional requirements",
    "guardrail": "Ethics and data guardrails",
    "mentor-principle": "Mentorship principles (concept)",
    "mentor-supply": "Mentorship supply tiers (concept)",
    "mentor-format": "Mentorship formats (concept)",
    "mentor-guardrail": "Mentorship safeguarding (concept)",
}

KIND_ORDER = list(KIND_LABEL)

OWNER_LABEL = {
    "eng": "Engineering",
    "product": "Product",
    "content": "Content",
    "research": "Research",
}

DASH = "\u2014"

REF_FIELDS = ("derives_from", "governs", "leads_to", "blocks", "affects")

CITATION_RE = re.compile(
    r"\b(?:GT|NFR|ADR|OQ|KPI|PG\d|CF|RK|MP|MS|ME|M\d|[PREDT])-(?:F)?\d+\b"
)
MODULE_RE = re.compile(r"\bM[1-7]\b")


class DataError(Exception):
    pass


# --------------------------------------------------------------------------
# model
# --------------------------------------------------------------------------


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise DataError(f"missing data file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        raise DataError(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")


class Model:
    def __init__(self, requirements: dict, roadmap: dict, decisions: dict):
        self.requirements = requirements
        self.roadmap = roadmap
        self.decisions = decisions
        self.items = [dict(i) for i in requirements.get("items", [])]
        self.by_id = {}
        self.raw_status = {
            i.get("id"): i.get("status") for i in requirements.get("items", [])
        }
        for item in self.items:
            item.setdefault("track", "delivery")
            item.setdefault("status", self._default_status(item))
            item.setdefault("evidence", [])
            item.setdefault("tracking", [])
            item.setdefault("updated", requirements.get("as_of"))
            self.by_id[item["id"]] = item
        self.children = {}
        for item in self.items:
            parent = item.get("parent")
            if parent:
                self.children.setdefault(parent, []).append(item)
        for item in self.items:
            if item["kind"] == "module" and self.children.get(item["id"]):
                item["status"] = self._rollup(self.children[item["id"]])
                item["rolled_up"] = True

    @staticmethod
    def _default_status(item: dict) -> str:
        return {"delivery": "not-started", "compliance": "not-applicable", "context": "reference"}[
            item.get("track", "delivery")
        ]

    @staticmethod
    def _rollup(children: list) -> str:
        live = [c for c in children if c.get("track") == "delivery"]
        statuses = {c.get("status", "not-started") for c in live}
        if not statuses:
            return "not-started"
        if statuses <= {"deferred", "concept"}:
            return "deferred"
        if "blocked" in statuses:
            return "blocked"
        real = statuses - {"deferred", "concept"}
        if real <= {"shipped", "verified"}:
            return "verified" if real == {"verified"} else "shipped"
        if real == {"not-started"}:
            return "not-started"
        return "in-progress"

    # -- lookups ----------------------------------------------------------

    @property
    def as_of(self) -> str:
        return self.roadmap.get("as_of") or self.requirements.get("as_of") or ""

    @property
    def current_phase(self) -> str:
        return str(self.roadmap.get("current_phase", "0"))

    def phase(self, phase_id: str) -> dict | None:
        for p in self.roadmap.get("phases", []):
            if str(p["id"]) == str(phase_id):
                return p
        return None

    def of_kind(self, kind: str) -> list:
        return [i for i in self.items if i["kind"] == kind]

    def vocab(self, item: dict) -> dict:
        return TRACK_VOCAB[item.get("track", "delivery")].get(
            item.get("status"), {"label": item.get("status", "?"), "icon": "\u2753", "tone": "idle"}
        )

    def known_ids(self) -> set:
        ids = set(self.by_id)
        for phase in self.roadmap.get("phases", []):
            ids.add(f"PHASE-{phase['id']}")
            ids.update(c["id"] for c in phase.get("exit_criteria", []))
        for key in ("content_floor", "metrics", "risks"):
            ids.update(entry["id"] for entry in self.roadmap.get(key, []))
        for group in self.roadmap.get("launch_checklists", {}).values():
            ids.update(entry["id"] for entry in group)
        for key in ("product_decisions", "adrs", "open_questions"):
            ids.update(entry["id"] for entry in self.decisions.get(key, []))
        return ids

    # -- progress ---------------------------------------------------------

    def progress(self, items: list) -> tuple:
        """(percent, done, counted) over delivery items that carry a weight."""
        counted = [
            i
            for i in items
            if i.get("track") == "delivery"
            and DELIVERY_STATUS.get(i.get("status"), {}).get("weight") is not None
        ]
        if not counted:
            return 0.0, 0, 0
        earned = sum(DELIVERY_STATUS[i["status"]]["weight"] for i in counted)
        done = sum(1 for i in counted if DELIVERY_STATUS[i["status"]]["weight"] == 1.0)
        return 100.0 * earned / len(counted), done, len(counted)

    def phase_items(self, phase_id: str) -> list:
        return [
            i
            for i in self.items
            if str(i.get("phase", "")) == str(phase_id) and i["kind"] in ("feature", "nfr")
        ]

    def mvp_items(self) -> list:
        return [i for i in self.items if i.get("mvp")]

    def guardrails(self) -> list:
        return [i for i in self.items if i.get("track") == "compliance"]

    def focus_items(self) -> list:
        return [i for i in self.items if i.get("focus")]


def load_model(base: Path = DATA) -> Model:
    return Model(
        load(base / "requirements.json"),
        load(base / "roadmap.json"),
        load(base / "decisions.json"),
    )


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------


def validate(model: Model) -> list:
    problems = []
    seen = set()
    phase_ids = {str(p["id"]) for p in model.roadmap.get("phases", [])}
    known = model.known_ids()

    for item in model.items:
        rid = item.get("id")
        where = f"requirements.json[{rid or '?'}]"
        if not rid:
            problems.append(f"{where}: item has no id")
            continue
        if rid in seen:
            problems.append(f"{where}: duplicate id")
        seen.add(rid)
        if item.get("kind") not in KIND_LABEL:
            problems.append(f"{where}: unknown kind {item.get('kind')!r}")
        track = item.get("track")
        if track not in TRACK_VOCAB:
            problems.append(f"{where}: unknown track {track!r}")
            continue
        if item.get("status") not in TRACK_VOCAB[track]:
            problems.append(
                f"{where}: status {item.get('status')!r} is not valid on the {track} track "
                f"(allowed: {', '.join(TRACK_VOCAB[track])})"
            )
        if not item.get("title"):
            problems.append(f"{where}: missing title")
        if not item.get("source"):
            problems.append(f"{where}: missing source reference")
        if item.get("phase") is not None and str(item["phase"]) not in phase_ids:
            problems.append(f"{where}: phase {item['phase']!r} is not a roadmap phase")
        if (
            item.get("kind") == "module"
            and model.children.get(rid)
            and model.raw_status.get(rid) is not None
        ):
            problems.append(
                f"{where}: module status is rolled up from its features - remove the manual status"
            )
        if item.get("track") == "compliance" and not item.get("violation_test"):
            problems.append(f"{where}: compliance items need a violation_test")
        for field in REF_FIELDS:
            for ref in item.get(field, []):
                if ref not in known:
                    problems.append(f"{where}: {field} points at unknown id {ref!r}")
        parent = item.get("parent")
        if parent and parent not in model.by_id:
            problems.append(f"{where}: parent {parent!r} does not exist")
        if item.get("updated") and not _is_iso_date(item["updated"]):
            problems.append(f"{where}: updated {item['updated']!r} is not YYYY-MM-DD")

    for phase in model.roadmap.get("phases", []):
        for crit in phase.get("exit_criteria", []):
            if crit.get("status") not in DELIVERY_STATUS:
                problems.append(
                    f"roadmap.json[{crit.get('id')}]: unknown status {crit.get('status')!r}"
                )

    for adr in model.decisions.get("adrs", []):
        if adr.get("status") not in {"proposed", "accepted", "superseded", "rejected"}:
            problems.append(f"decisions.json[{adr.get('id')}]: unknown ADR status {adr.get('status')!r}")
        for ref in adr.get("blocks", []) + adr.get("product_refs", []):
            if ref not in known:
                problems.append(f"decisions.json[{adr.get('id')}]: unknown reference {ref!r}")

    for entry in model.decisions.get("product_decisions", []) + model.decisions.get("open_questions", []):
        for ref in entry.get("affects", []) + entry.get("blocks", []):
            if ref not in known:
                problems.append(f"decisions.json[{entry.get('id')}]: unknown reference {ref!r}")

    return problems


def _is_iso_date(value: str) -> bool:
    try:
        dt.date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


# --------------------------------------------------------------------------
# small rendering helpers
# --------------------------------------------------------------------------


def bar(pct: float, width: int = 22) -> str:
    filled = int(round(pct / 100 * width))
    return "\u2588" * filled + "\u2591" * (width - filled)


def pct_str(pct: float) -> str:
    return f"{pct:.0f}%"


def badge(model: Model, item: dict) -> str:
    v = model.vocab(item)
    return f"{v['icon']} {v['label']}"


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def owner_of(item: dict) -> str:
    return OWNER_LABEL.get(item.get("owner"), item.get("owner") or "\u2014")


def refs(item: dict, field: str) -> str:
    values = item.get(field) or []
    return ", ".join(f"`{v}`" for v in values) if values else "\u2014"


def links(item: dict) -> str:
    out = [f"[{_link_label(u)}]({u})" for u in item.get("tracking", [])]
    out += [f"[{_link_label(u)}]({u})" for u in item.get("evidence", [])]
    return ", ".join(out) if out else "\u2014"


def _link_label(url: str) -> str:
    tail = url.rstrip("/").split("/")
    if len(tail) >= 2 and tail[-2] in ("issues", "pull"):
        return f"#{tail[-1]}"
    return tail[-1][:24]


# --------------------------------------------------------------------------
# markdown views
# --------------------------------------------------------------------------


def render_readme(model: Model) -> str:
    overall = model.progress([i for i in model.items if i["kind"] in ("feature", "nfr")])
    mvp = model.progress(model.mvp_items())
    phase = model.phase(model.current_phase)
    guards = model.guardrails()
    binding_guards = [g for g in guards if g.get("binding") is not False]
    upheld = sum(1 for g in binding_guards if g["status"] == "upheld")
    breached = [g for g in binding_guards if g["status"] in ("at-risk", "violated")]
    open_q = model.decisions.get("open_questions", [])
    open_adrs = [a for a in model.decisions.get("adrs", []) if a["status"] == "proposed"]

    L = [BANNER]
    L.append("# UFQ progress tracker\n")
    L.append(
        f"**Phase {model.current_phase} \u2014 {phase['name']}** \u00b7 as of {model.as_of} "
        f"\u00b7 [Roadmap](roadmap.md) \u00b7 [Requirements](requirements.md) "
        f"\u00b7 [Guardrails](guardrails.md) \u00b7 [Decisions](decisions.md)\n"
    )
    L.append(f"> {model.roadmap.get('state_of_play', '')}\n")

    L.append("## At a glance\n")
    L.append("| | Progress | |")
    L.append("|---|---|---|")
    L.append(f"| Delivery, all phases | `{bar(overall[0])}` | {pct_str(overall[0])} \u00b7 {overall[1]}/{overall[2]} done |")
    L.append(f"| MVP scope (Phase 1) | `{bar(mvp[0])}` | {pct_str(mvp[0])} \u00b7 {mvp[1]}/{mvp[2]} done |")
    L.append(
        f"| Binding guardrails upheld | `{bar(100.0 * upheld / len(binding_guards) if binding_guards else 0)}` "
        f"| {upheld}/{len(binding_guards)} \u00b7 {len(breached)} at risk or violated |"
    )
    L.append(f"| Open decisions | \u2014 | {len(open_adrs)} ADR, {len(open_q)} open questions |")
    L.append("")

    if breached:
        L.append("> [!WARNING]")
        L.append("> Guardrails needing attention: " + ", ".join(f"`{g['id']}`" for g in breached))
        L.append("")

    L.append("## Phases\n")
    L.append("| Phase | | Requirements | Exit criteria met |")
    L.append("|---|---|---|---|")
    for p in model.roadmap.get("phases", []):
        pi = model.progress(model.phase_items(p["id"]))
        crits = p.get("exit_criteria", [])
        met = sum(1 for c in crits if c.get("status") in ("shipped", "verified"))
        marker = "\u25b6\ufe0e" if str(p["id"]) == model.current_phase else "\u00a0"
        L.append(
            f"| {marker} **{p['id']} \u2014 {md_escape(p['name'])}** | `{bar(pi[0], 14)}` "
            f"| {pct_str(pi[0])} \u00b7 {pi[1]}/{pi[2]} | {met}/{len(crits)} |"
        )
    L.append("")

    focus = model.focus_items()
    if focus:
        L.append("## Now and next\n")
        L.append("| ID | Requirement | Status | Owner | Tracking |")
        L.append("|---|---|---|---|---|")
        for item in focus:
            L.append(
                f"| `{item['id']}` | {md_escape(item['title'])} | {badge(model, item)} "
                f"| {owner_of(item)} | {links(item)} |"
            )
        L.append("")

    L.append("## Module board\n")
    L.append("| Module | Phase | | Features |")
    L.append("|---|---|---|---|")
    for module in model.of_kind("module"):
        kids = model.children.get(module["id"], [])
        mp = model.progress(kids)
        counts = " ".join(
            model.vocab(k)["icon"] for k in kids if k.get("track") == "delivery"
        ) or DASH
        L.append(
            f"| {badge(model, module)} **[`{module['id']}` {md_escape(module['title'])}](requirements.md#modules)** "
            f"| {module.get('phase', DASH)} | `{bar(mp[0], 12)}` {pct_str(mp[0])} | {counts} |"
        )
    L.append("")
    L.append(
        "Feature icons in reading order: "
        + ", ".join(f"{v['icon']} {v['label'].lower()}" for v in DELIVERY_STATUS.values())
        + ".\n"
    )

    L.append("## Content floor\n")
    L.append("| Target | Phase | | Count |")
    L.append("|---|---|---|---|")
    for cf in model.roadmap.get("content_floor", []):
        p = 100.0 * cf["current"] / cf["target"] if cf["target"] else 0.0
        L.append(
            f"| {md_escape(cf['label'])} | {cf['phase']} | `{bar(min(p, 100), 14)}` "
            f"| {cf['current']}/{cf['target']} {cf['unit']} |"
        )
    L.append("")

    L.append("## How this stays true\n")
    L.append(
        "This tracker is generated from `docs/progress/data/*.json`. Edit the data in the same pull "
        "request as the work and reference the requirement IDs in the description - CI regenerates "
        "these views and commits them to your branch. A cited ID that does not exist fails the "
        "pull request. See [HOWTO.md](HOWTO.md).\n"
    )
    return "\n".join(L).rstrip() + "\n"


def anchor(text: str) -> str:
    return re.sub(r"[^a-z0-9\- ]", "", text.lower()).replace(" ", "-")


def render_roadmap(model: Model) -> str:
    L = [BANNER, "# Roadmap and gates\n"]
    L.append(f"As of {model.as_of}. [Back to the tracker](README.md).\n")

    for p in model.roadmap.get("phases", []):
        current = str(p["id"]) == model.current_phase
        pi = model.progress(model.phase_items(p["id"]))
        L.append(f"## Phase {p['id']} \u2014 {p['name']}" + ("  \u25b6\ufe0e current" if current else ""))
        L.append("")
        L.append(f"**Goal.** {p['goal']}\n")
        L.append(f"**Scope.** {p['scope']}\n")
        L.append(f"**Requirements in this phase.** `{bar(pi[0])}` {pct_str(pi[0])} \u00b7 {pi[1]}/{pi[2]} done\n")
        L.append("| Exit criterion | Target | Current | Status | Source |")
        L.append("|---|---|---|---|---|")
        for c in p.get("exit_criteria", []):
            v = DELIVERY_STATUS.get(c.get("status"), {"icon": "\u2753", "label": c.get("status")})
            L.append(
                f"| `{c['id']}` {md_escape(c['label'])} | {md_escape(c['target'])} "
                f"| {c.get('current') if c.get('current') is not None else 'no data yet'} "
                f"| {v['icon']} {v['label']} | {md_escape(c.get('source', ''))} |"
            )
        L.append("")

    L.append("## Content floor\n")
    L.append("| Target | Phase | Progress | Count | Source |")
    L.append("|---|---|---|---|---|")
    for cf in model.roadmap.get("content_floor", []):
        p = 100.0 * cf["current"] / cf["target"] if cf["target"] else 0.0
        L.append(
            f"| {md_escape(cf['label'])} | {cf['phase']} | `{bar(min(p, 100), 14)}` {pct_str(p)} "
            f"| {cf['current']}/{cf['target']} {cf['unit']} | {md_escape(cf.get('source', ''))} |"
        )
    L.append("")

    L.append("## Success metrics\n")
    L.append("Targets are provisional and confirmed at each phase start via the Decisions Log.\n")
    L.append("| ID | Phase | Metric | Target | Current |")
    L.append("|---|---|---|---|---|")
    for m in model.roadmap.get("metrics", []):
        L.append(
            f"| `{m['id']}` | {m['phase']} | {md_escape(m['label'])} | {md_escape(m['target'])} "
            f"| {m['current'] if m['current'] is not None else 'no data yet'} |"
        )
    L.append("")

    for phase_key, entries in model.roadmap.get("launch_checklists", {}).items():
        L.append(f"## Launch checklist \u2014 {phase_key.replace('-', ' ')}\n")
        for e in entries:
            L.append(f"- [{'x' if e['done'] else ' '}] `{e['id']}` {e['label']}")
        L.append("")

    L.append("## Risks and standing mitigations\n")
    L.append("| ID | Risk | Standing mitigation | Status |")
    L.append("|---|---|---|---|")
    for r in model.roadmap.get("risks", []):
        L.append(
            f"| `{r['id']}` | {md_escape(r['label'])} | {md_escape(r['mitigation'])} | {md_escape(r['status'])} |"
        )
    L.append("")
    return "\n".join(L).rstrip() + "\n"


def render_requirements(model: Model) -> str:
    L = [BANNER, "# Requirement register\n"]
    L.append(
        f"Every stable ID from the product framework and the mentorship concept, with its current "
        f"state. As of {model.as_of}. [Back to the tracker](README.md).\n"
    )
    L.append("**Contents:** " + " \u00b7 ".join(
        f"[{KIND_LABEL[k]}](#{anchor(KIND_LABEL[k])})" for k in KIND_ORDER if model.of_kind(k)
    ) + "\n")

    for kind in KIND_ORDER:
        items = model.of_kind(kind)
        if not items:
            continue
        L.append(f"## {KIND_LABEL[kind]}\n")
        if kind == "ground-truth":
            for i in items:
                L.append(f"### `{i['id']}` {i['title']}\n")
                L.append(f"{i['summary']}\n")
                L.append(f"**Design implication.** {i.get('implication', '')}\n")
                L.append(f"Leads to: {refs(i, 'leads_to')} \u00b7 Source: {i['source']}\n")
            continue
        if kind == "module":
            L.append("| ID | Module | Phase | Status | Features |")
            L.append("|---|---|---|---|---|")
            for i in items:
                kids = model.children.get(i["id"], [])
                mp = model.progress(kids)
                L.append(
                    f"| `{i['id']}` | {md_escape(i['title'])} "
                    f"| {i.get('phase', DASH)} | {badge(model, i)} "
                    f"| {mp[1]}/{mp[2]} done \u00b7 {pct_str(mp[0])} |"
                )
            L.append("")
            for i in items:
                L.append(f"- **`{i['id']}` {i['title']}** \u2014 {md_escape(i['summary'])}")
            L.append("")
            continue
        if kind == "role":
            L.append("| ID | Role | First phase | Description |")
            L.append("|---|---|---|---|")
            for i in items:
                L.append(
                    f"| `{i['id']}` | {md_escape(i['title'])} | {i.get('phase', DASH)} "
                    f"| {md_escape(i['summary'])} |"
                )
            L.append("")
            continue
        if kind in ("principle", "guardrail", "mentor-principle", "mentor-guardrail"):
            L.append("| ID | Rule | Status | Violation test |")
            L.append("|---|---|---|---|")
            for i in items:
                L.append(
                    f"| `{i['id']}` | **{md_escape(i['title'])}** \u2014 {md_escape(i['summary'])} "
                    f"| {badge(model, i)} | {md_escape(i.get('violation_test', ''))} |"
                )
            L.append("")
            continue

        L.append("| ID | Requirement | Phase | MVP | Status | Owner | Traces to | Links |")
        L.append("|---|---|---|---|---|---|---|---|")
        for i in items:
            L.append(
                f"| `{i['id']}` | **{md_escape(i['title'])}** \u2014 {md_escape(i['summary'])} "
                f"| {i.get('phase', DASH)} | {'yes' if i.get('mvp') else DASH} "
                f"| {badge(model, i)} | {owner_of(i)} | {refs(i, 'derives_from')} | {links(i)} |"
            )
        L.append("")
    return "\n".join(L).rstrip() + "\n"


def render_guardrails(model: Model) -> str:
    guards = model.guardrails()
    binding = [g for g in guards if g.get("binding") is not False]
    concept = [g for g in guards if g.get("binding") is False]

    L = [BANNER, "# Guardrail board\n"]
    L.append(
        "Binding rules and the concrete symptom that says we are drifting. A guardrail is never "
        "\u201cdone\u201d; it is upheld, at risk, or violated. Move a row to \u26a0\ufe0f or \U0001f6a8 "
        "in the same pull request that introduces the risk.\n"
    )
    L.append(f"As of {model.as_of}. [Back to the tracker](README.md).\n")

    counts = {}
    for g in binding:
        counts[g["status"]] = counts.get(g["status"], 0) + 1
    L.append(
        "**Binding:** "
        + " \u00b7 ".join(
            f"{COMPLIANCE_STATUS[s]['icon']} {counts[s]} {COMPLIANCE_STATUS[s]['label'].lower()}"
            for s in COMPLIANCE_STATUS
            if counts.get(s)
        )
        + "\n"
    )

    def table(rows, title, note=""):
        L.append(f"## {title}\n")
        if note:
            L.append(f"{note}\n")
        L.append("| ID | Guardrail | Status | Violation test | Governs | Source |")
        L.append("|---|---|---|---|---|---|")
        for g in rows:
            L.append(
                f"| `{g['id']}` | **{md_escape(g['title'])}** \u2014 {md_escape(g['summary'])} "
                f"| {badge(model, g)} | {md_escape(g.get('violation_test', ''))} "
                f"| {refs(g, 'governs')} | {md_escape(g['source'])} |"
            )
        L.append("")

    table([g for g in binding if g["kind"] == "principle"], "Design principles")
    table([g for g in binding if g["kind"] == "guardrail"], "Ethics and data guardrails")
    others = [g for g in binding if g["kind"] not in ("principle", "guardrail")]
    if others:
        table(others, "Product-level refusals")
    if concept:
        table(
            concept,
            "Mentorship (concept, not yet binding)",
            "From the mentorship concept document. These become binding only when a slice graduates "
            "into the framework's Decisions Log.",
        )
    return "\n".join(L).rstrip() + "\n"


def render_decisions(model: Model) -> str:
    d = model.decisions
    L = [BANNER, "# Decision ledger\n"]
    L.append(
        "Product decisions mirror the framework's Decisions Log, which stays authoritative. ADRs "
        "record implementation choices. Open questions are the things still costing us optionality.\n"
    )
    L.append(f"As of {model.as_of}. [Back to the tracker](README.md).\n")

    L.append("## Product decisions\n")
    L.append("| ID | Date | Decision | Rationale | Owner | Affects |")
    L.append("|---|---|---|---|---|---|")
    for e in d.get("product_decisions", []):
        L.append(
            f"| `{e['id']}` | {e['date']} | {md_escape(e['decision'])} | {md_escape(e['rationale'])} "
            f"| {md_escape(e['owner'])} | {refs(e, 'affects')} |"
        )
    L.append("")

    L.append("## Architecture decision records\n")
    L.append("| ID | Title | Status | Date | Product refs | Blocks | Tracking |")
    L.append("|---|---|---|---|---|---|---|")
    for a in d.get("adrs", []):
        track = f"[{_link_label(a['tracking'])}]({a['tracking']})" if a.get("tracking") else "\u2014"
        L.append(
            f"| `{a['id']}` | {md_escape(a['title'])} | {a['status']} | {a.get('date') or DASH} "
            f"| {refs(a, 'product_refs')} | {refs(a, 'blocks')} | {track} |"
        )
    L.append("")

    L.append("## Open questions\n")
    L.append("| ID | Area | Question | Blocks | Source |")
    L.append("|---|---|---|---|---|")
    for q in d.get("open_questions", []):
        L.append(
            f"| `{q['id']}` | {q['area']} | {md_escape(q['question'])} | {refs(q, 'blocks')} "
            f"| {md_escape(q['source'])} |"
        )
    L.append("")
    L.append(
        "Open-question IDs are assigned by this tracker for reference; they are not IDs from the "
        "source documents.\n"
    )
    return "\n".join(L).rstrip() + "\n"


VIEWS = {
    "README.md": render_readme,
    "roadmap.md": render_roadmap,
    "requirements.md": render_requirements,
    "guardrails.md": render_guardrails,
    "decisions.md": render_decisions,
}


# --------------------------------------------------------------------------
# build / check
# --------------------------------------------------------------------------


def build_all(model: Model) -> dict:
    """The views that live in the repository. The HTML dashboard is deliberately
    not one of them - see `html`, and docs/progress/HOWTO.md."""
    return {name: fn(model) for name, fn in VIEWS.items()}


def cmd_build(args) -> int:
    model = load_model()
    problems = validate(model)
    if problems:
        _report(problems)
        return 1
    for name, content in build_all(model).items():
        (OUT / name).write_text(content, encoding="utf-8")
        print(f"wrote docs/progress/{name}")
    return 0


def cmd_validate(args) -> int:
    problems = validate(load_model())
    if problems:
        _report(problems)
        return 1
    print("progress data is valid")
    return 0


def cmd_check(args) -> int:
    model = load_model()
    problems = validate(model)
    stale = []
    for name, content in build_all(model).items():
        path = OUT / name
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            stale.append(name)
    if stale:
        problems.append(
            "generated views are stale: "
            + ", ".join(f"docs/progress/{n}" for n in stale)
            + "\n    run: python3 tools/progress/progress.py build, then commit the result"
        )
    if problems:
        _report(problems)
        return 1
    print("progress data is valid and every generated view is current")
    return 0


def _report(problems: list) -> None:
    print(f"progress tracker: {len(problems)} problem(s)\n", file=sys.stderr)
    for p in problems:
        print(f"  - {p}", file=sys.stderr)
    print(
        "\nsee docs/progress/HOWTO.md for the data format and the update workflow",
        file=sys.stderr,
    )


# --------------------------------------------------------------------------
# citations and the PR report
# --------------------------------------------------------------------------


def gather_text(args) -> str:
    chunks = []
    for path in args.text_file or []:
        p = Path(path)
        if p.exists():
            chunks.append(p.read_text(encoding="utf-8", errors="replace"))
    if args.text:
        chunks.append(args.text)
    if args.base:
        chunks.append(git("log", "--format=%s%n%b", f"{args.base}..HEAD"))
    return "\n".join(chunks)


def git(*cmd: str) -> str:
    try:
        return subprocess.run(
            ["git", *cmd], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def cited_ids(text: str, known: set) -> tuple:
    """(ids present in the registry, tokens that look like IDs but are not)."""
    found = set(CITATION_RE.findall(text)) | set(MODULE_RE.findall(text))
    return sorted(i for i in found if i in known), sorted(i for i in found if i not in known)


def cmd_cite_check(args) -> int:
    model = load_model()
    known = model.known_ids()
    text = gather_text(args)
    ok, unknown = cited_ids(text, known)
    if unknown:
        _report(
            [
                "cited requirement IDs that do not exist: "
                + ", ".join(unknown)
                + "\n    check the spelling, or add the requirement to "
                "docs/progress/data/requirements.json"
            ]
        )
        return 1
    print(f"{len(ok)} cited requirement ID(s) resolve" if ok else "no requirement IDs cited")
    return 0


def base_model(base_ref: str, model: Model) -> Model | None:
    blob = git("show", f"{base_ref}:docs/progress/data/requirements.json")
    if not blob.strip():
        return None
    try:
        return Model(json.loads(blob), model.roadmap, model.decisions)
    except json.JSONDecodeError:
        return None


def status_delta(before: Model | None, after: Model) -> list:
    if before is None:
        return []
    rows = []
    for item in after.items:
        old = before.by_id.get(item["id"])
        if old is None:
            rows.append((item["id"], item["title"], None, item["status"], after.vocab(item)))
        elif old["status"] != item["status"]:
            rows.append((item["id"], item["title"], old["status"], item["status"], after.vocab(item)))
    return rows


MARKER = "<!-- ufq-progress-tracker -->"


def cmd_pr_report(args) -> int:
    model = load_model()
    known = model.known_ids()
    text = gather_text(args)
    ok, unknown = cited_ids(text, known)
    before = base_model(args.base, model) if args.base else None
    delta = status_delta(before, model)

    L = [MARKER, "### Progress tracker\n"]

    if delta:
        L.append("**Status changes in this pull request**\n")
        L.append("| ID | Requirement | Was | Now |")
        L.append("|---|---|---|---|")
        for rid, title, old, new, vocab in delta:
            old_label = (
                TRACK_VOCAB["delivery"].get(old, TRACK_VOCAB["compliance"].get(old, {})).get("label", old)
                if old
                else "new"
            )
            L.append(f"| `{rid}` | {md_escape(title)} | {old_label} | {vocab['icon']} {vocab['label']} |")
        L.append("")
    else:
        L.append(
            "No requirement status changed in this pull request. If that is wrong, update "
            "`docs/progress/data/requirements.json` and run `python3 tools/progress/progress.py build`.\n"
        )

    if ok:
        L.append("<details><summary><b>Requirements referenced</b> "
                 f"({len(ok)})</summary>\n")
        L.append("| ID | Requirement | Status |")
        L.append("|---|---|---|")
        for rid in ok:
            item = model.by_id.get(rid)
            if item:
                L.append(f"| `{rid}` | {md_escape(item['title'])} | {badge(model, item)} |")
            else:
                L.append(f"| `{rid}` | — | — |")
        L.append("\n</details>\n")
    else:
        L.append(
            "> No requirement IDs referenced. If this change implements or affects a product "
            "requirement, cite its ID (for example `M1-F3`, `E-8`, `ADR-0001`) in the description.\n"
        )

    if unknown:
        L.append("> [!CAUTION]")
        L.append("> Referenced IDs that do not exist: " + ", ".join(f"`{u}`" for u in unknown) + "\n")

    phase = model.phase(model.current_phase)
    pi = model.progress(model.phase_items(model.current_phase))
    mvp = model.progress(model.mvp_items())
    guards = [g for g in model.guardrails() if g.get("binding") is not False]
    breached = [g for g in guards if g["status"] in ("at-risk", "violated")]
    L.append(
        f"**Phase {model.current_phase} — {phase['name']}** `{bar(pi[0], 16)}` {pct_str(pi[0])} "
        f"({pi[1]}/{pi[2]})  ·  **MVP** `{bar(mvp[0], 16)}` {pct_str(mvp[0])} ({mvp[1]}/{mvp[2]})"
    )
    if breached:
        L.append(
            "\n⚠️ Guardrails needing attention: " + ", ".join(f"`{g['id']}`" for g in breached)
        )
    if args.repo_url:
        base = args.repo_url.rstrip("/") + "/blob/main/docs/progress"
        L.append(
            f"\n[Tracker]({base}/README.md) · [Guardrails]({base}/guardrails.md) · "
            f"[Decisions]({base}/decisions.md)"
        )

    body = "\n".join(L)
    if args.out:
        Path(args.out).write_text(body, encoding="utf-8")
    else:
        print(body)
    return 0


def cmd_html(args) -> int:
    model = load_model()
    sys.stdout.write(render_html.render(model, standalone=not args.fragment))
    return 0


# --------------------------------------------------------------------------


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("build", help="regenerate every view").set_defaults(fn=cmd_build)
    sub.add_parser("validate", help="check the data only").set_defaults(fn=cmd_validate)
    sub.add_parser("check", help="validate and fail if any view is stale").set_defaults(fn=cmd_check)

    for name, fn, helptext in (
        ("cite-check", cmd_cite_check, "fail if a cited requirement ID does not exist"),
        ("pr-report", cmd_pr_report, "write the pull-request comment body"),
    ):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("--base", help="base git ref, for commit messages and the status delta")
        p.add_argument("--text", help="extra text to scan for requirement IDs")
        p.add_argument("--text-file", action="append", help="file whose text is scanned (repeatable)")
        if name == "pr-report":
            p.add_argument("--out", help="write the comment body here instead of stdout")
            p.add_argument("--repo-url", help="repository URL, used to build absolute links")
        p.set_defaults(fn=fn)

    p = sub.add_parser("html", help="render the dashboard to stdout")
    p.add_argument("--fragment", action="store_true", help="omit the document shell (for Artifacts)")
    p.set_defaults(fn=cmd_html)

    args = parser.parse_args(argv)
    try:
        return args.fn(args)
    except DataError as exc:
        _report([str(exc)])
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
