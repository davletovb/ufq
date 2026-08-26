#!/usr/bin/env python3
"""Renders the progress dashboard.

Design note: the page is achromatic except for status. Requirement IDs are set
in mono because the ID system is how this project talks about itself; the only
chroma on the page is delivery and compliance state, so anything that needs
attention is the only thing that shouts.
"""

from __future__ import annotations

import html
import json

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Archivo:wght@400;500;600;700&"
    "family=IBM+Plex+Mono:wght@400;500;600&"
    "family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&"
    'display=swap">'
)

LIGHT_TOKENS = """
    --paper:#eef1f0; --surface:#ffffff; --surface-2:#f7f9f8;
    --ink:#0f1917; --ink-2:#3a4a47; --muted:#66756f; --line:#d8e0dd; --line-2:#e8eeec;
    --done:#1c6f47; --done-bg:#e0efe7; --active:#8f5a06; --active-bg:#f7ecda;
    --bad:#a52a20; --bad-bg:#f8e3e0; --idle:#7f8d89; --idle-bg:#eaeeec;
    --focus:#1f5fd0; --shadow:0 1px 2px rgba(15,25,23,.05),0 8px 24px -16px rgba(15,25,23,.25);
"""

DARK_TOKENS = """
    --paper:#0b1211; --surface:#111a19; --surface-2:#16211f;
    --ink:#e7edeb; --ink-2:#c2cecb; --muted:#8fa09b; --line:#25322f; --line-2:#1c2725;
    --done:#5cb98a; --done-bg:#14291f; --active:#dda63f; --active-bg:#2b2214;
    --bad:#ef8177; --bad-bg:#2e1a18; --idle:#8b9995; --idle-bg:#1b2523;
    --focus:#6f9dff; --shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px -16px rgba(0,0,0,.8);
"""

CSS = """
*,*::before,*::after{box-sizing:border-box}
:root{%LIGHT%
  --f-ui:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif;
  --f-read:"Newsreader",Georgia,"Times New Roman",serif;
  --f-mono:"IBM Plex Mono",ui-monospace,"SF Mono",Menlo,monospace;
  --w:1180px;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){%DARK%}}
:root[data-theme="dark"]{%DARK%}

body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--f-ui);
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
a{color:inherit;text-underline-offset:3px;text-decoration-color:var(--line)}
a:hover{text-decoration-color:currentColor}
:focus-visible{outline:2px solid var(--focus);outline-offset:2px;border-radius:3px}
h1,h2,h3{text-wrap:balance;margin:0;font-weight:600;letter-spacing:-.011em}
p{margin:0}
table{border-collapse:collapse;width:100%;font-size:13.5px}
code,.mono{font-family:var(--f-mono);font-variant-ligatures:none}

.wrap{max-width:var(--w);margin:0 auto;padding:0 24px 96px;
  display:grid;grid-template-columns:190px minmax(0,1fr);gap:44px;align-items:start}
@media (max-width:900px){.wrap{grid-template-columns:1fr;gap:0}}

/* masthead ---------------------------------------------------------- */
.masthead{border-bottom:1px solid var(--line);background:var(--surface)}
.masthead-in{max-width:var(--w);margin:0 auto;padding:38px 24px 30px}
.eyebrow{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--muted);display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.eyebrow .sep{color:var(--line)}
h1{font-size:clamp(30px,4.4vw,46px);line-height:1.03;margin:14px 0 0;letter-spacing:-.03em}
.standfirst{font-family:var(--f-read);font-size:clamp(17px,2vw,20px);line-height:1.45;
  color:var(--ink-2);max-width:62ch;margin:14px 0 0;font-weight:300}

/* nav --------------------------------------------------------------- */
nav.rail{position:sticky;top:0;padding:36px 0 0;font-size:13px}
@media (max-width:900px){nav.rail{position:static;padding:24px 0 0;
  border-bottom:1px solid var(--line);margin-bottom:8px}}
nav.rail ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1px}
@media (max-width:900px){nav.rail ol{flex-direction:row;flex-wrap:wrap;gap:2px 16px;padding-bottom:20px}}
nav.rail a{display:flex;gap:9px;padding:5px 0;color:var(--muted);text-decoration:none;
  border-bottom:1px solid transparent}
nav.rail a:hover{color:var(--ink)}
nav.rail a.on{color:var(--ink);font-weight:500}
nav.rail .n{font-family:var(--f-mono);font-size:11px;color:var(--line);padding-top:2px}
nav.rail a:hover .n,nav.rail a.on .n{color:var(--muted)}

/* sections ---------------------------------------------------------- */
main{padding-top:36px;min-width:0}
section{scroll-margin-top:20px;margin-bottom:52px}
.sec-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;
  border-bottom:1px solid var(--ink);padding-bottom:7px;margin-bottom:18px;flex-wrap:wrap}
.sec-head h2{font-size:19px;letter-spacing:-.015em}
.sec-head .note{font-size:12px;color:var(--muted);font-family:var(--f-mono)}
.lede{font-family:var(--f-read);font-weight:300;font-size:16.5px;color:var(--ink-2);
  max-width:64ch;margin-bottom:20px}

/* tiles ------------------------------------------------------------- */
.tiles{display:flex;flex-wrap:wrap;gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:2px;overflow:hidden}
.tile{background:var(--surface);padding:16px 18px 18px;display:flex;flex-direction:column;gap:9px;
  flex:1 1 168px;min-width:0}
.tile .k{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.tile .v{font-size:29px;line-height:1;font-weight:600;letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.tile .v small{font-size:14px;font-weight:400;color:var(--muted);letter-spacing:0}
.tile .sub{font-size:12px;color:var(--muted)}

/* meter ------------------------------------------------------------- */
.meter{height:5px;background:var(--line-2);border-radius:99px;overflow:hidden;position:relative}
.meter i{display:block;height:100%;background:var(--ink);border-radius:99px}
.meter.is-done i{background:var(--done)}
.meter.is-active i{background:var(--active)}
.meter.thin{height:4px}

/* status pills ------------------------------------------------------ */
.pill{display:inline-flex;align-items:center;gap:6px;padding:2.5px 9px 2.5px 7px;border-radius:99px;
  font-size:11.5px;font-weight:500;white-space:nowrap;line-height:1.5;
  background:var(--idle-bg);color:var(--idle)}
.pill::before{content:"";width:6px;height:6px;border-radius:99px;background:currentColor;flex:none}
.pill.done{background:var(--done-bg);color:var(--done)}
.pill.active{background:var(--active-bg);color:var(--active)}
.pill.bad{background:var(--bad-bg);color:var(--bad)}
.pill.warn{background:var(--active-bg);color:var(--active)}
.pill.muted{background:var(--idle-bg);color:var(--muted);opacity:.85}
.pill.ghost::before{opacity:.45}

/* tables ------------------------------------------------------------ */
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:2px;background:var(--surface)}
th{text-align:left;font-family:var(--f-mono);font-size:10.5px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--muted);font-weight:500;padding:10px 14px;
  border-bottom:1px solid var(--line);white-space:nowrap;background:var(--surface-2)}
td{padding:11px 14px;border-bottom:1px solid var(--line-2);vertical-align:top}
tr:last-child td{border-bottom:0}
tbody tr:hover td{background:var(--surface-2)}
td.id{font-family:var(--f-mono);font-size:12px;font-weight:500;white-space:nowrap;color:var(--ink)}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
td .t{font-weight:500}
td .d{color:var(--muted);font-size:12.5px;line-height:1.45;margin-top:2px;max-width:60ch}
td .test{color:var(--ink-2);font-size:12.5px;max-width:46ch}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin-top:5px}
.chip{font-family:var(--f-mono);font-size:10.5px;padding:1px 6px;border:1px solid var(--line);
  border-radius:2px;color:var(--muted);white-space:nowrap}
.w-meter{width:150px}

/* module board ------------------------------------------------------ */
.modules{display:flex;flex-wrap:wrap;gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:2px;overflow:hidden}
.mod{background:var(--surface);padding:16px 18px;display:flex;flex-direction:column;gap:11px;
  flex:1 1 268px;min-width:0}
.mod-top{display:flex;align-items:center;justify-content:space-between;gap:10px}
.mod-id{font-family:var(--f-mono);font-size:11.5px;color:var(--muted)}
.mod h3{font-size:15.5px;letter-spacing:-.012em}
.mod .desc{font-size:12.5px;color:var(--muted);line-height:1.45;flex:1}
.dots{display:flex;flex-wrap:wrap;gap:4px}
.dot{width:9px;height:9px;border-radius:2px;background:var(--idle-bg);
  border:1px solid var(--line);position:relative}
.dot.done{background:var(--done);border-color:var(--done)}
.dot.active{background:var(--active);border-color:var(--active)}
.dot.bad{background:var(--bad);border-color:var(--bad)}
.dot.muted{background:var(--line-2);border-color:var(--line)}
.mod .count{font-family:var(--f-mono);font-size:11px;color:var(--muted);
  display:flex;justify-content:space-between}

/* gates ------------------------------------------------------------- */
.gate{border:1px solid var(--line);border-radius:2px;background:var(--surface);margin-bottom:14px;
  overflow:hidden}
.gate.current{border-color:var(--ink)}
.gate-head{display:flex;align-items:center;gap:14px;padding:14px 18px;flex-wrap:wrap;
  background:var(--surface-2);border-bottom:1px solid var(--line)}
.gate-head .ph{font-family:var(--f-mono);font-size:11px;color:var(--muted);letter-spacing:.1em;
  text-transform:uppercase}
.gate-head h3{font-size:16px;flex:1;min-width:180px}
.gate-body{padding:15px 18px 17px;display:grid;gap:13px}
.goal{font-family:var(--f-read);font-weight:300;font-size:15.5px;color:var(--ink-2);max-width:62ch}
.crit{display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:6px 14px;align-items:baseline;
  padding-top:11px;border-top:1px solid var(--line-2)}
@media (max-width:560px){.crit{grid-template-columns:minmax(0,1fr) auto}}
.crit .lab{font-size:13.5px}
.crit .lab .cid{font-family:var(--f-mono);font-size:11px;color:var(--muted);margin-right:7px}
.crit .tgt{font-family:var(--f-mono);font-size:12px;color:var(--muted);
  font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}

/* ground truths ----------------------------------------------------- */
.truths{display:grid;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:2px}
.truth{background:var(--surface);padding:15px 18px;display:grid;
  grid-template-columns:62px minmax(0,1fr);gap:18px}
@media (max-width:640px){.truth{grid-template-columns:1fr;gap:6px}}
.truth .gid{font-family:var(--f-mono);font-size:12px;font-weight:500;color:var(--muted);padding-top:2px}
.truth h3{font-size:14.5px;margin-bottom:4px}
.truth p{font-size:13px;color:var(--muted);line-height:1.5;max-width:66ch}
.truth .imp{font-family:var(--f-read);font-size:14px;font-weight:300;color:var(--ink-2);
  margin-top:7px;padding-left:13px;border-left:2px solid var(--line);max-width:62ch}

/* filter bar -------------------------------------------------------- */
.filters{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:14px}
.filters input{font:inherit;font-size:13px;padding:6px 11px;border:1px solid var(--line);
  border-radius:2px;background:var(--surface);color:var(--ink);min-width:210px}
.filters input::placeholder{color:var(--muted)}
.fbtn{font:inherit;font-size:12px;padding:5px 11px;border:1px solid var(--line);border-radius:99px;
  background:var(--surface);color:var(--muted);cursor:pointer}
.fbtn[aria-pressed="true"]{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.fbtn:hover{color:var(--ink)}
.fbtn[aria-pressed="true"]:hover{color:var(--paper)}
.empty{padding:22px;text-align:center;color:var(--muted);font-size:13px;display:none}
.empty.on{display:block}

/* misc -------------------------------------------------------------- */
.legend{display:flex;gap:14px;flex-wrap:wrap;margin-top:12px;font-size:11.5px;color:var(--muted)}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{width:9px;height:9px;border-radius:2px;display:inline-block}
.callout{border:1px solid var(--bad);background:var(--bad-bg);color:var(--bad);
  padding:12px 16px;border-radius:2px;font-size:13.5px;margin-bottom:18px}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:22px}
footer{max-width:var(--w);margin:0 auto;padding:26px 24px 60px;border-top:1px solid var(--line);
  color:var(--muted);font-size:12.5px;display:flex;gap:18px;flex-wrap:wrap;justify-content:space-between}
footer code{font-size:11.5px;color:var(--ink-2)}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

TONE_CLASS = {"done": "done", "active": "active", "bad": "bad", "warn": "warn", "idle": "", "muted": "muted"}


def esc(text) -> str:
    return html.escape(str(text if text is not None else ""), quote=True)


def pill(vocab: dict, ghost: bool = False) -> str:
    cls = TONE_CLASS.get(vocab.get("tone", "idle"), "")
    return (
        f'<span class="pill {cls}{" ghost" if ghost else ""}">{esc(vocab["label"])}</span>'
    )


def meter(pct: float, tone: str = "", thin: bool = False) -> str:
    cls = " ".join(x for x in (("is-" + tone) if tone else "", "thin" if thin else "") if x)
    return (
        f'<div class="meter {cls}" role="img" aria-label="{pct:.0f} percent">'
        f'<i style="width:{max(0.0, min(pct, 100.0)):.1f}%"></i></div>'
    )


def tone_of(model, item) -> str:
    return model.vocab(item).get("tone", "idle")


# --------------------------------------------------------------------------


def render(model, standalone: bool = True) -> str:
    from progress import DELIVERY_STATUS, OWNER_LABEL  # local import avoids a cycle

    r = model.roadmap
    phase = model.phase(model.current_phase) or {}
    overall = model.progress([i for i in model.items if i["kind"] in ("feature", "nfr")])
    mvp = model.progress(model.mvp_items())
    phase_p = model.progress(model.phase_items(model.current_phase))
    guards = [g for g in model.guardrails() if g.get("binding") is not False]
    upheld = sum(1 for g in guards if g["status"] == "upheld")
    breached = [g for g in guards if g["status"] in ("at-risk", "violated")]
    open_adrs = [a for a in model.decisions.get("adrs", []) if a["status"] == "proposed"]
    open_q = model.decisions.get("open_questions", [])

    sections = []

    # -- state of play ----------------------------------------------------
    tiles = [
        (
            "Phase " + esc(model.current_phase),
            esc(phase.get("name", "")),
            f"{sum(1 for c in phase.get('exit_criteria', []) if c.get('status') in ('shipped', 'verified'))}"
            f"/{len(phase.get('exit_criteria', []))} exit criteria met",
            None,
        ),
        (
            "Requirements delivered",
            f"{overall[0]:.0f}<small>%</small>",
            f"{overall[1]} of {overall[2]} tracked",
            (overall[0], "done" if overall[0] >= 100 else "active" if overall[0] > 0 else ""),
        ),
        (
            "MVP scope",
            f"{mvp[0]:.0f}<small>%</small>",
            f"{mvp[1]} of {mvp[2]} Phase-1 requirements",
            (mvp[0], "done" if mvp[0] >= 100 else "active" if mvp[0] > 0 else ""),
        ),
        (
            "Guardrails upheld",
            f"{upheld}<small>/{len(guards)}</small>",
            f"{len(breached)} at risk or violated" if breached else "none at risk",
            None,
        ),
        (
            "Open decisions",
            f"{len(open_adrs) + len(open_q)}",
            f"{len(open_adrs)} ADR, {len(open_q)} open questions",
            None,
        ),
    ]
    tile_html = []
    for k, v, sub, m in tiles:
        bar_html = meter(m[0], m[1], thin=True) if m else ""
        tile_html.append(
            f'<div class="tile"><span class="k">{k}</span>'
            f'<span class="v">{v}</span>{bar_html}<span class="sub">{sub}</span></div>'
        )
    body = f'<div class="tiles">{"".join(tile_html)}</div>'
    if breached:
        body = (
            '<div class="callout"><b>Guardrails needing attention:</b> '
            + ", ".join(f"<code>{esc(g['id'])}</code> {esc(g['title'])}" for g in breached)
            + "</div>"
            + body
        )
    sections.append((
        "state",
        "State of play",
        f"phase {esc(model.current_phase)} of 3",
        "",
        body,
    ))

    # -- phase gates ------------------------------------------------------
    gates = []
    for p in r.get("phases", []):
        current = str(p["id"]) == model.current_phase
        pp = model.progress(model.phase_items(p["id"]))
        crits = "".join(
            '<div class="crit"><div class="lab">'
            f'<span class="cid">{esc(c["id"])}</span>{esc(c["label"])}</div>'
            f'<div>{pill(DELIVERY_STATUS.get(c.get("status"), {"label": c.get("status"), "tone": "idle"}), ghost=True)}</div>'
            f'<div class="tgt">{esc(c["target"])}'
            + (f' &middot; now {esc(c["current"])}' if c.get("current") is not None else "")
            + "</div></div>"
            for c in p.get("exit_criteria", [])
        )
        gates.append(
            f'<article class="gate{" current" if current else ""}">'
            f'<div class="gate-head"><span class="ph">Phase {esc(p["id"])}</span>'
            f'<h3>{esc(p["name"])}</h3>'
            + (f'<span class="pill active">Current</span>' if current else
               f'<span class="pill muted">{esc(p.get("status", "planned")).title()}</span>')
            + f'<span class="mod-id">{pp[1]}/{pp[2]} requirements</span></div>'
            f'<div class="gate-body"><p class="goal">{esc(p["goal"])}</p>'
            + meter(pp[0], "done" if pp[0] >= 100 else "active" if pp[0] > 0 else "")
            + crits
            + "</div></article>"
        )
    sections.append(
        (
            "gates",
            "Phase gates",
            "exit criteria from framework §10 and §11.4",
            "A phase ends when its exit criteria are met, not when the work feels finished.",
            "".join(gates),
        )
    )

    # -- module board -----------------------------------------------------
    cards = []
    for m in model.of_kind("module"):
        kids = model.children.get(m["id"], [])
        mp = model.progress(kids)
        dots = "".join(
            f'<span class="dot {TONE_CLASS.get(tone_of(model, k), "")}" title="{esc(k["id"])} '
            f'{esc(k["title"])}: {esc(model.vocab(k)["label"])}"></span>'
            for k in kids
            if k.get("track") == "delivery"
        )
        cards.append(
            f'<article class="mod"><div class="mod-top"><span class="mod-id">{esc(m["id"])}'
            f'&nbsp;&nbsp;phase {esc(m.get("phase", "-"))}</span>{pill(model.vocab(m))}</div>'
            f'<h3>{esc(m["title"])}</h3>'
            f'<p class="desc">{esc(m["summary"])}</p>'
            + (f'<div class="dots">{dots}</div>' if dots else "")
            + meter(mp[0], "done" if mp[0] >= 100 else "active" if mp[0] > 0 else "", thin=True)
            + f'<div class="count"><span>{mp[1]}/{mp[2]} requirements</span>'
            f"<span>{mp[0]:.0f}%</span></div></article>"
        )
    legend = '<div class="legend">' + "".join(
        f'<span><i class="dot {TONE_CLASS.get(v["tone"], "")}" style="border:1px solid var(--line)"></i>'
        f'{esc(v["label"])}</span>'
        for v in DELIVERY_STATUS.values()
    ) + "</div>"
    sections.append(
        (
            "modules",
            "Module board",
            "one square per functional requirement",
            "Module state is rolled up from its requirements, never set by hand.",
            f'<div class="modules">{"".join(cards)}</div>{legend}',
        )
    )

    # -- register ---------------------------------------------------------
    rows = []
    for item in model.items:
        if item["kind"] not in ("feature", "nfr"):
            continue
        v = model.vocab(item)
        traces = "".join(f'<span class="chip">{esc(t)}</span>' for t in item.get("derives_from", []))
        linked = "".join(
            f'<a class="chip" href="{esc(u)}">{esc(_short(u))}</a>'
            for u in item.get("tracking", []) + item.get("evidence", [])
        )
        rows.append(
            f'<tr data-status="{esc(item["status"])}" data-text="{esc((item["id"] + " " + item["title"] + " " + item["summary"]).lower())}">'
            f'<td class="id">{esc(item["id"])}</td>'
            f'<td><div class="t">{esc(item["title"])}</div>'
            f'<div class="d">{esc(item["summary"])}</div>'
            + (f'<div class="chips">{traces}{linked}</div>' if traces or linked else "")
            + "</td>"
            f'<td>{pill(v)}</td>'
            f'<td class="num">{esc(item.get("phase", "-"))}{"" if not item.get("mvp") else " · MVP"}</td>'
            f'<td class="num">{esc(OWNER_LABEL.get(item.get("owner"), item.get("owner") or "-"))}</td>'
            "</tr>"
        )
    status_buttons = "".join(
        f'<button class="fbtn" type="button" data-status="{esc(k)}" aria-pressed="false">'
        f'{esc(v["label"])}</button>'
        for k, v in DELIVERY_STATUS.items()
    )
    register = (
        '<div class="filters">'
        '<input id="q" type="search" placeholder="Filter by ID, title or text" aria-label="Filter requirements">'
        f"{status_buttons}"
        '<button class="fbtn" type="button" id="clear">Reset</button></div>'
        '<div class="scroll"><table id="reg"><thead><tr>'
        "<th>ID</th><th>Requirement</th><th>Status</th><th>Phase</th><th>Owner</th>"
        f'</tr></thead><tbody>{"".join(rows)}</tbody></table>'
        '<div class="empty" id="none">Nothing matches that filter.</div></div>'
    )
    sections.append(
        (
            "register",
            "Requirement register",
            f"{len(rows)} functional and non-functional requirements",
            "Every requirement that has to be built, with the ground truth it descends from.",
            register,
        )
    )

    # -- guardrails -------------------------------------------------------
    def guard_table(items, caption):
        if not items:
            return ""
        body = "".join(
            f'<tr><td class="id">{esc(g["id"])}</td>'
            f'<td><div class="t">{esc(g["title"])}</div><div class="d">{esc(g["summary"])}</div></td>'
            f'<td>{pill(model.vocab(g))}</td>'
            f'<td><div class="test">{esc(g.get("violation_test", ""))}</div></td></tr>'
            for g in items
        )
        return (
            f'<h3 style="font-size:13px;font-family:var(--f-mono);text-transform:uppercase;'
            f'letter-spacing:.11em;color:var(--muted);margin:22px 0 9px">{esc(caption)}</h3>'
            f'<div class="scroll"><table><thead><tr><th>ID</th><th>Rule</th><th>State</th>'
            f'<th>Violation test</th></tr></thead><tbody>{body}</tbody></table></div>'
        )

    guard_html = (
        guard_table([g for g in guards if g["kind"] == "principle"], "Design principles")
        + guard_table([g for g in guards if g["kind"] == "guardrail"], "Ethics and data guardrails")
        + guard_table(
            [g for g in guards if g["kind"] not in ("principle", "guardrail")],
            "Product-level refusals",
        )
        + guard_table(
            [g for g in model.guardrails() if g.get("binding") is False],
            "Mentorship, concept - not yet binding",
        )
    )
    sections.append(
        (
            "guardrails",
            "Guardrail board",
            "a guardrail is never done",
            "Each rule carries the concrete symptom that says we are drifting. Rows move to at risk "
            "or violated in the same pull request that introduces the risk.",
            guard_html,
        )
    )

    # -- ground truths ----------------------------------------------------
    truths = "".join(
        f'<article class="truth"><div class="gid">{esc(t["id"])}</div><div>'
        f'<h3>{esc(t["title"])}</h3><p>{esc(t["summary"])}</p>'
        f'<p class="imp">{esc(t.get("implication", ""))}</p>'
        f'<div class="chips">'
        + "".join(f'<span class="chip">{esc(x)}</span>' for x in t.get("leads_to", []))
        + "</div></div></article>"
        for t in model.of_kind("ground-truth")
    )
    sections.append(
        (
            "truths",
            "Ground truths",
            "constraints, not opinions",
            "The context the design must absorb. Changing one requires a Decisions Log entry; the "
            "chips are the requirements that descend from it.",
            f'<div class="truths">{truths}</div>',
        )
    )

    # -- decisions --------------------------------------------------------
    d = model.decisions
    dec_rows = "".join(
        f'<tr><td class="id">{esc(e["id"])}</td><td class="num">{esc(e["date"])}</td>'
        f'<td><div class="t">{esc(e["decision"])}</div><div class="d">{esc(e["rationale"])}</div>'
        + (
            '<div class="chips">'
            + "".join(f'<span class="chip">{esc(a)}</span>' for a in e.get("affects", []))
            + "</div>"
            if e.get("affects")
            else ""
        )
        + f'</td><td class="num">{esc(e["owner"])}</td></tr>'
        for e in d.get("product_decisions", [])
    )
    adr_rows = "".join(
        f'<tr><td class="id">{esc(a["id"])}</td>'
        f'<td><div class="t">{esc(a["title"])}</div>'
        + (
            '<div class="chips">'
            + "".join(f'<span class="chip">blocks {esc(b)}</span>' for b in a.get("blocks", []))
            + "</div>"
            if a.get("blocks")
            else ""
        )
        + "</td>"
        f'<td><span class="pill {"active" if a["status"] == "proposed" else "done"}">'
        f'{esc(a["status"]).title()}</span></td>'
        + (
            f'<td><a class="chip" href="{esc(a["tracking"])}">{esc(_short(a["tracking"]))}</a></td>'
            if a.get("tracking")
            else "<td></td>"
        )
        + "</tr>"
        for a in d.get("adrs", [])
    )
    oq_rows = "".join(
        f'<tr><td class="id">{esc(q["id"])}</td>'
        f'<td><div class="t">{esc(q["question"])}</div>'
        + (
            '<div class="chips">'
            + "".join(f'<span class="chip">blocks {esc(b)}</span>' for b in q.get("blocks", []))
            + "</div>"
            if q.get("blocks")
            else ""
        )
        + f'</td><td class="num">{esc(q["area"])}</td></tr>'
        for q in d.get("open_questions", [])
    )
    sections.append(
        (
            "decisions",
            "Decision ledger",
            "product decisions, ADRs, open questions",
            "The framework's Decisions Log stays authoritative for product decisions; ADRs cover "
            "implementation. Open questions are what still costs us optionality.",
            '<div class="scroll"><table><thead><tr><th>ID</th><th>Date</th><th>Decision</th>'
            f'<th>Owner</th></tr></thead><tbody>{dec_rows}</tbody></table></div>'
            '<h3 style="font-size:13px;font-family:var(--f-mono);text-transform:uppercase;'
            'letter-spacing:.11em;color:var(--muted);margin:22px 0 9px">Architecture decision records</h3>'
            '<div class="scroll"><table><thead><tr><th>ID</th><th>Decision</th><th>Status</th>'
            f'<th>Tracking</th></tr></thead><tbody>{adr_rows}</tbody></table></div>'
            '<h3 style="font-size:13px;font-family:var(--f-mono);text-transform:uppercase;'
            'letter-spacing:.11em;color:var(--muted);margin:22px 0 9px">Open questions</h3>'
            f'<div class="scroll"><table><thead><tr><th>ID</th><th>Question</th><th>Area</th>'
            f'</tr></thead><tbody>{oq_rows}</tbody></table></div>',
        )
    )

    # -- content and metrics ---------------------------------------------
    floor = "".join(
        f'<div class="crit"><div class="lab"><span class="cid">{esc(c["id"])}</span>'
        f'{esc(c["label"])} <span style="color:var(--muted)">· phase {esc(c["phase"])}</span></div>'
        f'<div class="tgt">{c["current"]}/{c["target"]} {esc(c["unit"])}</div>'
        f'<div style="grid-column:1/-1">'
        + meter(100.0 * c["current"] / c["target"] if c["target"] else 0.0, "active", thin=True)
        + "</div></div>"
        for c in r.get("content_floor", [])
    )
    kpis = "".join(
        f'<tr><td class="id">{esc(m["id"])}</td><td>{esc(m["label"])}</td>'
        f'<td class="num">{esc(m["phase"])}</td><td class="num">{esc(m["target"])}</td>'
        f'<td class="num" style="color:var(--muted)">'
        f'{esc(m["current"]) if m["current"] is not None else "no data yet"}</td></tr>'
        for m in r.get("metrics", [])
    )
    sections.append(
        (
            "outcomes",
            "Content floor and outcomes",
            "targets confirmed at each phase start",
            "The content library is the moat, so its floor is tracked like code. Outcome metrics stay "
            "empty until there is real data - an empty column is information.",
            f'<div class="cols"><div><div class="gate"><div class="gate-body">{floor}</div></div></div>'
            f'<div><div class="scroll"><table><thead><tr><th>ID</th><th>Metric</th><th>Phase</th>'
            f'<th>Target</th><th>Current</th></tr></thead><tbody>{kpis}</tbody></table></div></div></div>',
        )
    )

    # -- assemble ---------------------------------------------------------
    nav = "".join(
        f'<li><a href="#{sid}">{esc(title)}</a></li>'
        for sid, title, _, _, _ in sections
    )
    main = "".join(
        f'<section id="{sid}"><div class="sec-head"><h2>{esc(title)}</h2>'
        + (f'<span class="note">{esc(note)}</span>' if note else "")
        + "</div>"
        + (f'<p class="lede">{lede}</p>' if lede else "")
        + content
        + "</section>"
        for sid, title, note, lede, content in sections
    )

    masthead = (
        '<header class="masthead"><div class="masthead-in">'
        '<div class="eyebrow"><span>UFQ</span><span class="sep">/</span>'
        "<span>Career discovery platform, Uzbekistan</span>"
        f'<span class="sep">/</span><span>as of {esc(model.as_of)}</span></div>'
        "<h1>Progress tracker</h1>"
        f'<p class="standfirst">{esc(r.get("state_of_play", ""))}</p>'
        "</div></header>"
    )

    footer = (
        "<footer><span>Generated from <code>docs/progress/data/*.json</code> by "
        "<code>tools/progress/progress.py</code>. Updated in the same pull request as the work.</span>"
        f"<span>Phase {esc(model.current_phase)} · {phase_p[1]}/{phase_p[2]} requirements delivered</span>"
        "</footer>"
    )

    css = CSS.replace("%LIGHT%", LIGHT_TOKENS).replace("%DARK%", DARK_TOKENS)
    head = f"<title>UFQ Progress Tracker</title>\n{FONTS}\n<style>{css}</style>"
    page = (
        f'{masthead}<div class="wrap"><nav class="rail" aria-label="Sections"><ol>{nav}</ol></nav>'
        f"<main>{main}</main></div>{footer}\n<script>{JS}</script>"
    )
    if not standalone:
        # Artifacts supply the document shell; emit head content then page content.
        return f"{head}\n{page}\n"
    return (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        f"{head}\n</head>\n<body>\n{page}\n</body>\n</html>\n"
    )


def _short(url: str) -> str:
    parts = url.rstrip("/").split("/")
    if len(parts) >= 2 and parts[-2] in ("issues", "pull"):
        return f"#{parts[-1]}"
    return parts[-1][:22]


JS = """
(function(){
  var q=document.getElementById('q'), tbl=document.getElementById('reg');
  if(!q||!tbl) return;
  var rows=[].slice.call(tbl.tBodies[0].rows),
      btns=[].slice.call(document.querySelectorAll('.fbtn[data-status]')),
      none=document.getElementById('none'), active={};
  function apply(){
    var term=q.value.trim().toLowerCase(),
        want=Object.keys(active).filter(function(k){return active[k]}), shown=0;
    rows.forEach(function(r){
      var ok=(!term||r.dataset.text.indexOf(term)>-1) &&
             (!want.length||want.indexOf(r.dataset.status)>-1);
      r.hidden=!ok; if(ok) shown++;
    });
    none.classList.toggle('on', shown===0);
    try{localStorage.setItem('ufq.filter',JSON.stringify({t:term,s:want}))}catch(e){}
  }
  btns.forEach(function(b){
    b.addEventListener('click',function(){
      active[b.dataset.status]=!active[b.dataset.status];
      b.setAttribute('aria-pressed', active[b.dataset.status]?'true':'false');
      apply();
    });
  });
  q.addEventListener('input',apply);
  document.getElementById('clear').addEventListener('click',function(){
    q.value=''; active={}; btns.forEach(function(b){b.setAttribute('aria-pressed','false')}); apply();
  });
  try{
    var s=JSON.parse(localStorage.getItem('ufq.filter')||'{}');
    if(s.t){q.value=s.t}
    (s.s||[]).forEach(function(k){
      active[k]=true;
      var b=document.querySelector('.fbtn[data-status="'+k+'"]');
      if(b) b.setAttribute('aria-pressed','true');
    });
  }catch(e){}
  apply();
  var links=[].slice.call(document.querySelectorAll('nav.rail a')),
      secs=links.map(function(a){return document.querySelector(a.getAttribute('href'))});
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(!e.isIntersecting) return;
        var i=secs.indexOf(e.target);
        links.forEach(function(a,j){a.classList.toggle('on', i===j)});
      });
    },{rootMargin:'-10% 0px -80% 0px'});
    secs.forEach(function(s){if(s) io.observe(s)});
  }
})();
"""
