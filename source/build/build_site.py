# -*- coding: utf-8 -*-
"""Assemble the five WeYield artifacts into one static site for Vercel."""
import io, os, re, shutil, sys

SRC = r"C:\Users\shobh\AppData\Local\Temp\claude\C--Users-shobh\475cfc18-8d30-4031-a0be-040218d182a7\scratchpad\weyield"
OUT = r"E:\weyield-advisory"

PAGES = [
    # slug,           source file,          nav label,        n, question it answers
    ("five-moves",    "five-moves.html",    "Five Moves",     "1",
     "What is actually wrong, and what are the five things to do about it?"),
    ("monday-brief",  "monday-brief.html",  "Monday Brief",   "2",
     "What ships first, and exactly how does it work?"),
    ("residual-radar","residual-radar.html","Residual Radar", "3",
     "Where the profit really sits — and where the used-car data comes from."),
    ("agentic-gtm",   "agentic-gtm.html",   "Agentic GTM",    "4",
     "How does a nine-person company reach six hundred operators?"),
    ("tech-stack",    "tech-stack.html",    "Tech Stack",     "5",
     "What do two engineers build it on?"),
]

CARD_POINTS = {
    "five-moves": [
        "Five decisions run a car rental business. At Hertz each has a department; at a 300-car operator each has the owner.",
        "Two moves raise revenue per account, two change how many accounts WeYield can reach.",
        "Seven diagrams, including the servable-floor curve that explains why the market “is” 600–1,000.",
    ],
    "monday-brief": [
        "A weekly brief to the owner in a coach's voice — three actions, each with a euro value.",
        "Deterministic facts pack, coach-owned rules, a verifier that drops any sentence whose numbers don't match.",
        "Eight weeks, two engineers, ~€0.12 a brief, no new integration and no user interface.",
    ],
    "residual-radar": [
        "The residual pool is ~€14M against €336K of annual profit. A 5% miss is two years of profit.",
        "Diesel is a policy cliff with years of warning. Electric is a price shock with none. Opposite responses.",
        "Every named data feed — Autovista, Indicata, the free LEZ registry — and which to open first.",
    ],
    "agentic-gtm": [
        "At today's rate the gap closes in 34 years. Agent-assisted reps get it to 15. Structure gets it to 3.",
        "Seven agents, autonomy granted by consequence: research free, sending gated, commitments never.",
        "€15K a year — 17% of one salesperson — and it unlocks two motions no rep can deliver.",
    ],
    "tech-stack": [
        "Seven rules that settle the next fifty technology arguments, starting with the 3am test.",
        "The strangler seam: a shared warehouse, and write-back only through the existing API.",
        "Three things are built — facts builder, rules engine, verifier. Everything else is bought.",
    ],
}

DOCS = [
    ("Building the AI-Native Business",
     "The full strategy — why the product is capped, the three-horizon plan, the kill-risks, the financial shape.",
     "https://docs.google.com/document/d/1iQSuJYMgsaXIxJb6D2mAlHmENs-kCT6BQcEkIkl9UL8/edit", "Google Doc"),
    ("Meeting record, 10 Sep 2026 — English",
     "Olivier Jager's own strategic review, translated, with notes on where the French carries weight the English flattens.",
     "https://docs.google.com/document/d/1aC1ShK6GCExt4E5apfbiB5vMhe9qAwxPBI7mawjeKfM/edit", "Google Doc"),
]

DEFS = '<svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute"><defs><marker id="c-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker><marker id="c-arA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/></marker></defs></svg>\n'

FAVICON = ('data:image/svg+xml,'
           '<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22>'
           '<text y=%22.92em%22 font-size=%2290%22>%F0%9F%9A%99</text></svg>')

# monday-brief was authored before the pack settled on its palette; remap its
# tokens so the five pages read as one set. Colour only — typography untouched.
MB_OVERRIDE = """
/* --- pack palette override (site build) --- */
:root{
  --bg:#EFF1F2; --paper:#FFFFFF; --sunk:#E4E8EA; --mono-bg:#E4E8EA;
  --ink:#111A1E; --ink-2:#39474D; --muted:#6E7C82; --line:#CBD3D6; --line-2:#E1E7E9;
  --accent:#0B5D6E; --accent-ink:#FFFFFF; --accent-soft:#DCECEF;
  --warm:#B3661A; --warm-soft:#F7E9DA; --warm-ink:#7A3B10;
  --ok:#1D7049; --ok-soft:#DEEDE5; --amber:#B3661A; --amber-soft:#F7E9DA;
  --bad:#A8341C; --bad-soft:#F7E3DE;
  --shadow:0 1px 2px rgba(17,26,30,.05),0 14px 34px -20px rgba(17,26,30,.28);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#0C1315; --paper:#141F23; --sunk:#0F1A1D; --mono-bg:#0F1A1D;
    --ink:#E6EDEF; --ink-2:#BCCACF; --muted:#8698A0; --line:#2A3B41; --line-2:#1D2B30;
    --accent:#4FC2D4; --accent-ink:#08181C; --accent-soft:#12363E;
    --warm:#E0A25C; --warm-soft:#3A2A17; --warm-ink:#FFD9CF;
    --ok:#59C08C; --ok-soft:#16352A; --amber:#E0A25C; --amber-soft:#3A2E14;
    --bad:#EE8468; --bad-soft:#3D1E16;
    --shadow:0 1px 2px rgba(0,0,0,.5),0 14px 34px -20px rgba(0,0,0,.8);
  }
}
:root[data-theme="dark"]{
  --bg:#0C1315; --paper:#141F23; --sunk:#0F1A1D; --mono-bg:#0F1A1D;
  --ink:#E6EDEF; --ink-2:#BCCACF; --muted:#8698A0; --line:#2A3B41; --line-2:#1D2B30;
  --accent:#4FC2D4; --accent-ink:#08181C; --accent-soft:#12363E;
  --warm:#E0A25C; --warm-soft:#3A2A17; --warm-ink:#FFD9CF;
  --ok:#59C08C; --ok-soft:#16352A; --amber:#E0A25C; --amber-soft:#3A2E14;
  --bad:#EE8468; --bad-soft:#3D1E16;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 14px 34px -20px rgba(0,0,0,.8);
}
"""

NAV_CSS = """
/* --- pack navigation (site build) --- */
.pack-nav{position:sticky;top:0;z-index:80;display:flex;align-items:center;gap:4px 14px;
  padding:10px 30px;background:var(--paper);border-bottom:1px solid var(--line);flex-wrap:wrap;
  font-family:Archivo,system-ui,-apple-system,"Segoe UI",sans-serif}
.pack-nav .home{font-weight:700;font-size:14px;color:var(--ink);text-decoration:none;
  letter-spacing:-.01em;padding-right:16px;border-right:1px solid var(--line);white-space:nowrap}
.pack-nav .home span{color:var(--muted);font-weight:500}
.pack-nav .links{display:flex;gap:3px;flex-wrap:wrap;flex:1 1 auto}
.pack-nav .links a{font-size:12.5px;font-weight:500;color:var(--muted);text-decoration:none;
  padding:5px 11px;border-radius:5px;white-space:nowrap;line-height:1.3}
.pack-nav .links a:hover{color:var(--ink);background:var(--sunk,var(--line-2))}
.pack-nav .links a[aria-current="page"]{color:var(--accent-ink);background:var(--accent);font-weight:600}
.pack-nav .tog{flex:0 0 auto;font-family:inherit;font-size:12px;font-weight:600;letter-spacing:.06em;
  text-transform:uppercase;color:var(--muted);background:none;border:1px solid var(--line);
  border-radius:5px;padding:5px 10px;cursor:pointer;line-height:1.3}
.pack-nav .tog:hover{color:var(--ink);border-color:var(--muted)}
@media (max-width:700px){
  .pack-nav{padding:9px 18px;gap:4px 10px}
  .pack-nav .home{border-right:none;padding-right:0;width:100%}
  .pack-nav .links a{font-size:12px;padding:4px 8px}
}
@media print{.pack-nav{display:none}}
"""

THEME_SCRIPT = """<script>
(function(){try{var t=localStorage.getItem('wy-theme');
if(t==='dark'||t==='light'){document.documentElement.setAttribute('data-theme',t);}}catch(e){}})();
</script>"""

TOGGLE_SCRIPT = """<script>
(function(){
  var r=document.documentElement, b=document.getElementById('wy-tog');
  if(!b)return;
  function cur(){var a=r.getAttribute('data-theme');if(a)return a;
    return window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}
  function paint(){b.textContent=cur()==='dark'?'Light':'Dark';
    b.setAttribute('aria-label','Switch to '+(cur()==='dark'?'light':'dark')+' theme');}
  paint();
  b.addEventListener('click',function(){var n=cur()==='dark'?'light':'dark';
    r.setAttribute('data-theme',n);try{localStorage.setItem('wy-theme',n);}catch(e){}paint();});
})();
</script>"""


NAV_ITEMS = [("deck", "Deck")] + [(slug, label) for slug, _f, label, _n, _q in PAGES]


def nav_html(active):
    links = "".join(
        '<a href="/%s"%s>%s</a>' % (slug, ' aria-current="page"' if slug == active else "", label)
        for slug, label in NAV_ITEMS
    )
    return (
        '<nav class="pack-nav" aria-label="Advisory pack">'
        '<a class="home" href="/">WeYield <span>· advisory pack</span></a>'
        '<div class="links">%s</div>'
        '<button class="tog" id="wy-tog" type="button">Dark</button>'
        "</nav>" % links
    )


HEAD_BASE = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="%s">
<style>:root{color-scheme:light dark}*{box-sizing:border-box}img{max-width:100%%}[hidden]{display:none!important}</style>
""" % FAVICON


def build_page(slug, srcfile, active):
    raw = io.open(os.path.join(SRC, srcfile), encoding="utf-8").read()
    i = raw.index("</style>") + len("</style>")
    head_part, body_part = raw[:i], raw[i:]
    title = re.search(r"<title>(.*?)</title>", head_part, re.S).group(1).strip()
    extra = MB_OVERRIDE if slug == "monday-brief" else ""
    doc = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        + HEAD_BASE + THEME_SCRIPT + "\n" + head_part
        + "\n<style>" + extra + NAV_CSS + "</style>\n</head>\n<body>\n"
        + nav_html(active) + "\n" + body_part.strip() + "\n" + TOGGLE_SCRIPT + "\n</body>\n</html>\n"
    )
    io.open(os.path.join(OUT, slug + ".html"), "w", encoding="utf-8").write(doc)
    return title


def build_index(titles):
    cards = []
    for slug, _f, label, n, q in PAGES:
        pts = "".join("<li>%s</li>" % p for p in CARD_POINTS[slug])
        cards.append(
            '<a class="card" href="/%s"><div class="n">%s</div><div class="c">'
            "<h3>%s</h3><p class=\"q\">%s</p><ul>%s</ul>"
            '<span class="go">Open →</span></div></a>' % (slug, n, titles[slug], q, pts)
        )
    docs = "".join(
        '<a class="doc" href="%s" target="_blank" rel="noopener"><b>%s</b>'
        '<span class="kind">%s ↗</span><span class="d">%s</span></a>' % (u, t, k, d)
        for t, d, u, k in DOCS
    )
    body = """<header class="hero">
  <div class="wrap">
    <span class="eyebrow">Prepared for Emmanuel Scuto · by Ram Badrinathan · September 2026</span>
    <h1>WeYield<br><em>the AI-native advisory pack</em></h1>
    <p class="thesis">Five decisions run a car rental business. At Hertz, each one has a department. At a 300-car
      operator, each one has the owner — and only two of the five have a vendor in the room.
      <b>A deck, then five documents.</b></p>
  </div>
</header>

<section class="context">
  <div class="wrap">
    <div class="secline"><span class="eyebrow">Context</span><span class="rule"></span><span class="eyebrow">What this pack is, and how the pieces fit</span></div>

    <div class="ctx-grid">
      <div class="ctx">
        <h3>The question</h3>
        <p>Following the strategic review of 10 September 2026, the question put to me was a narrow one:
          <b>how does WeYield become AI-native</b> — not by adding features to what exists, but by changing
          what it sells, who it sells to, and what it costs to serve them.</p>
        <p>These six documents are the answer. They are written to be argued with.</p>
      </div>
      <div class="ctx">
        <h3>What it is not</h3>
        <p>Not a diligence exercise. <b>Nothing here has been verified against WeYield's accounts or systems</b>,
          and there is no financial model behind it.</p>
        <p>Product facts come from weyield.io and the September review. Everything else is derived arithmetic or a
          stated assumption — captions say which, and anything marked <em>illustrative</em> is the shape of an
          argument rather than a projection.</p>
      </div>
      <div class="ctx">
        <h3>Where to start</h3>
        <p>Not with code. Three facts would collapse most of what follows: <b>how much of the customer base still
          sits on OEM buyback</b>, whether fleet financials actually reach the integrated PMS systems, and the
          median fleet size across the base.</p>
        <p>Ten customer calls settle all three inside a week. That is the first move, and it costs nothing.</p>
      </div>
    </div>

    <figure class="ctx-fig">
      <svg viewBox="0 0 1200 396" role="img" aria-label="How the six documents relate. The deck compresses the whole argument and expands into Five Moves, the diagnosis and portfolio. Three deeper documents sit under it: Monday Brief which ships first and is the shared engine, Residual Radar the Horizon 2 product, and Agentic GTM the go-to-market infrastructure. The Monday Brief engine is reused by the other two, and Tech Stack is the substrate under everything.">
        <text x="0" y="14" class="tm" font-size="11" font-weight="600" letter-spacing="1.3">HOW THE SIX FIT TOGETHER</text>

        <rect x="0" y="28" width="1200" height="56" rx="7" class="fa"/>
        <text x="20" y="52" class="ti" font-size="15" font-weight="700">Deck</text>
        <text x="90" y="52" class="ti" font-size="13.5">The whole argument, compressed &mdash; 21 slides, about fifteen minutes</text>
        <text x="20" y="72" class="ti" font-size="12" opacity=".85">Start here on a call. Everything below is one of its sections, opened up.</text>
        <text x="1180" y="52" class="ti" font-size="12" font-weight="600" text-anchor="end">START HERE</text>

        <line x1="600" y1="86" x2="600" y2="102" class="sm" stroke-width="1.4" color="var(--muted)" marker-end="url(#c-ar)"/>

        <rect x="0" y="106" width="1200" height="56" rx="7" class="fp sa" stroke-width="1.6"/>
        <text x="20" y="130" class="ta" font-size="15" font-weight="700">Five Moves</text>
        <text x="135" y="130" font-size="13.5">The diagnosis &mdash; and the five things to do about it</text>
        <text x="20" y="150" class="tm" font-size="12">Two moves raise revenue per account; two change how many accounts WeYield can reach; one is the engine.</text>

        <line x1="182" y1="164" x2="182" y2="188" class="sm" stroke-width="1.4" color="var(--muted)" marker-end="url(#c-ar)"/>
        <line x1="600" y1="164" x2="600" y2="188" class="sm" stroke-width="1.4" color="var(--muted)" marker-end="url(#c-ar)"/>
        <line x1="1018" y1="164" x2="1018" y2="188" class="sm" stroke-width="1.4" color="var(--muted)" marker-end="url(#c-ar)"/>

        <rect x="0" y="192" width="388" height="96" rx="7" class="fp sl" stroke-width="1"/>
        <text x="20" y="216" font-size="14" font-weight="700">Monday Brief</text>
        <text x="20" y="236" class="tm" font-size="12.5">Ships first &mdash; eight weeks, two engineers,</text>
        <text x="20" y="253" class="tm" font-size="12.5">no new integration, no interface.</text>
        <text x="20" y="275" class="ta" font-size="12.5" font-weight="600">And it is the engine the other two reuse.</text>

        <rect x="406" y="192" width="388" height="96" rx="7" class="fp sl" stroke-width="1"/>
        <text x="426" y="216" font-size="14" font-weight="700">Residual Radar</text>
        <text x="426" y="236" class="tm" font-size="12.5">The Horizon 2 product &mdash; the buy-versus-sell</text>
        <text x="426" y="253" class="tm" font-size="12.5">decision, where the operator's year is decided.</text>
        <text x="426" y="275" class="tm" font-size="12.5">Includes every named used-car data feed.</text>

        <rect x="812" y="192" width="388" height="96" rx="7" class="fp sl" stroke-width="1"/>
        <text x="832" y="216" font-size="14" font-weight="700">Agentic GTM</text>
        <text x="832" y="236" class="tm" font-size="12.5">The infrastructure under the two reach moves.</text>
        <text x="832" y="253" class="tm" font-size="12.5">Seven agents, autonomy granted by consequence.</text>
        <text x="832" y="275" class="tm" font-size="12.5">Not a productivity play &mdash; a precondition.</text>

        <path d="M194 296 L194 314 L1006 314 L1006 296" class="fn sa" stroke-width="1.5" stroke-dasharray="5 4"/>
        <path d="M194 296 L194 314 L600 314" class="fn sa" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#c-arA)"/>
        <text x="600" y="332" class="ta" font-size="12.5" font-weight="600" text-anchor="middle">facts builder &rarr; rules engine &rarr; composer &rarr; verifier &mdash; built once, shared by all three</text>

        <rect x="0" y="344" width="1200" height="48" rx="7" class="fs"/>
        <text x="20" y="374" font-size="14" font-weight="700">Tech Stack</text>
        <text x="128" y="374" class="tm" font-size="13">What all of it is built on &mdash; sized to two engineers, additive to the existing product, nothing rewritten.</text>
      </svg>
    </figure>
  </div>
</section>

<section class="pack">
  <div class="wrap">
    <div class="secline"><span class="eyebrow">Start here</span><span class="rule"></span><span class="eyebrow">21 slides · about 15 minutes</span></div>
    <a class="deckcard" href="/deck">
      <div class="shot"><img src="/slides/t01.webp" alt="Deck cover slide" width="240" height="135" loading="eager"></div>
      <div class="c">
        <h3>Building the AI-Native WeYield</h3>
        <p class="q">The whole argument, in presentation form.</p>
        <ul><li>Why the current product is structurally capped, and what the market pays for the profile it produces.</li>
        <li>The recommendation: change the object, the buyer and the cost-to-serve — in that order.</li>
        <li>Three horizons, three kill-risks, and six decisions for Monday.</li></ul>
        <span class="go">Open the deck →</span>
      </div>
    </a>
    <div class="secline"><span class="eyebrow">Then go deeper</span><span class="rule"></span><span class="eyebrow">Five documents, in reading order</span></div>
    <div class="cards">%s</div>
  </div>
</section>

<section class="companions">
  <div class="wrap">
    <div class="secline"><span class="eyebrow">Companion documents</span><span class="rule"></span><span class="eyebrow">Google · anyone with the link can edit</span></div>
    <div class="docs">%s</div>
  </div>
</section>

<footer>
  <div class="wrap">
    <p><b>How to read the numbers.</b> Figures attributed to WeYield come from Olivier Jager's strategic review
      of 10 September 2026 and from weyield.io. Everything else across these documents is derived arithmetic or a
      stated assumption, built to show a mechanism and its order of magnitude rather than to forecast. Anything
      marked <em>illustrative</em> in a caption is the shape of an argument, not a projection. Replace every
      estimate with WeYield's own before any of it reaches a customer, a partner or an investor.</p>
    <p style="margin-top:12px"><b>Confidential.</b> Prepared for WeYield. Not indexed, not for onward circulation.</p>
  </div>
</footer>""" % ("".join(cards), docs)

    css = """
:root{
  --bg:#EFF1F2; --paper:#FFFFFF; --sunk:#E4E8EA;
  --ink:#111A1E; --ink-2:#39474D; --muted:#6E7C82; --line:#CBD3D6; --line-2:#E1E7E9;
  --accent:#0B5D6E; --accent-soft:#DCECEF; --accent-ink:#FFFFFF;
  --shadow:0 1px 2px rgba(17,26,30,.05),0 14px 34px -20px rgba(17,26,30,.28);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0C1315; --paper:#141F23; --sunk:#0F1A1D;
  --ink:#E6EDEF; --ink-2:#BCCACF; --muted:#8698A0; --line:#2A3B41; --line-2:#1D2B30;
  --accent:#4FC2D4; --accent-soft:#12363E; --accent-ink:#08181C;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 14px 34px -20px rgba(0,0,0,.8);
}}
:root[data-theme="dark"]{
  --bg:#0C1315; --paper:#141F23; --sunk:#0F1A1D;
  --ink:#E6EDEF; --ink-2:#BCCACF; --muted:#8698A0; --line:#2A3B41; --line-2:#1D2B30;
  --accent:#4FC2D4; --accent-soft:#12363E; --accent-ink:#08181C;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 14px 34px -20px rgba(0,0,0,.8);
}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Source Serif 4",Georgia,serif;font-size:16.5px;line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3,.eyebrow,.go,.n,.kind{font-family:Archivo,system-ui,-apple-system,"Segoe UI",sans-serif}
h1,h3{margin:0;text-wrap:balance;letter-spacing:-.02em;line-height:1.06}
p{margin:0 0 1em}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.wrap{max-width:1080px;margin:0 auto;padding:0 30px}
.eyebrow{font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}

.hero{padding:64px 0 44px}
.hero h1{font-size:clamp(40px,6.4vw,78px);font-weight:700;margin:16px 0 0}
.hero h1 em{font-style:normal;font-weight:500;color:var(--accent)}
.thesis{font-size:clamp(17px,2vw,20px);line-height:1.5;max-width:56ch;color:var(--ink-2);margin:22px 0 0}
.thesis b{color:var(--ink);font-weight:600}

section{padding:0 0 52px}
.secline{display:flex;align-items:center;gap:16px;padding:26px 0 20px;border-top:1px solid var(--line)}
.secline .rule{flex:1;height:1px;background:var(--line-2)}

.cards{display:grid;gap:14px}
.card{display:grid;grid-template-columns:64px minmax(0,1fr);gap:0 22px;align-items:start;
  background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:22px 26px;
  text-decoration:none;color:inherit;box-shadow:var(--shadow);transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--accent);transform:translateY(-1px)}
.card .n{width:44px;height:44px;border-radius:9px;background:var(--accent);color:var(--accent-ink);
  display:grid;place-items:center;font-size:19px;font-weight:700}
.card h3{font-size:clamp(21px,2.4vw,27px);font-weight:600}
.card .q{font-size:16px;color:var(--accent);margin:6px 0 0;font-style:italic}
.card ul{margin:13px 0 0;padding-left:1.05em;font-size:15px;color:var(--ink-2)}
.card li{margin-bottom:.35em}
.card .go{display:inline-block;margin-top:14px;font-size:12.5px;font-weight:600;
  letter-spacing:.06em;text-transform:uppercase;color:var(--accent)}

.context{padding-bottom:8px}
.ctx-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;margin-bottom:30px}
.ctx h3{font-size:18px;font-weight:600;margin-bottom:9px}
.ctx p{font-size:15px;color:var(--ink-2);margin:0 0 .75em;max-width:none}
.ctx p:last-child{margin:0}
.ctx b{color:var(--ink);font-weight:600}
.ctx-fig{margin:0;background:var(--paper);border:1px solid var(--line);border-radius:10px;
  padding:20px 22px 14px;box-shadow:var(--shadow)}
.ctx-fig svg{display:block;width:100%;max-width:100%;height:auto}
.ctx-fig svg text{font-family:Archivo,system-ui,sans-serif;fill:var(--ink)}
.ctx-fig svg .tm{fill:var(--muted)} .ctx-fig svg .ta{fill:var(--accent)} .ctx-fig svg .ti{fill:var(--accent-ink)}
.ctx-fig svg .fp{fill:var(--paper)} .ctx-fig svg .fs{fill:var(--sunk)} .ctx-fig svg .fa{fill:var(--accent)}
.ctx-fig svg .fn{fill:none}
.ctx-fig svg .sl{stroke:var(--line)} .ctx-fig svg .sa{stroke:var(--accent)} .ctx-fig svg .sm{stroke:var(--muted)}
@media (max-width:900px){.ctx-grid{grid-template-columns:1fr;gap:22px}}
.deckcard{display:grid;grid-template-columns:264px minmax(0,1fr);gap:0 26px;align-items:start;
  background:var(--paper);border:1px solid var(--accent);border-radius:10px;padding:22px 26px;
  text-decoration:none;color:inherit;box-shadow:var(--shadow);transition:transform .15s;margin-bottom:8px}
.deckcard:hover{transform:translateY(-1px)}
.deckcard .shot img{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:6px}
.deckcard h3{font-size:clamp(21px,2.4vw,27px);font-weight:600}
.deckcard .q{font-size:16px;color:var(--accent);margin:6px 0 0;font-style:italic}
.deckcard ul{margin:13px 0 0;padding-left:1.05em;font-size:15px;color:var(--ink-2)}
.deckcard li{margin-bottom:.35em}
.deckcard .go{display:inline-block;margin-top:14px;font-size:12.5px;font-weight:600;
  letter-spacing:.06em;text-transform:uppercase;color:var(--accent)}
@media (max-width:820px){.deckcard{grid-template-columns:1fr;gap:16px}}
.docs{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}
.doc{display:block;background:var(--paper);border:1px solid var(--line);border-radius:10px;
  padding:20px 22px;text-decoration:none;color:inherit;transition:border-color .15s}
.doc:hover{border-color:var(--accent)}
.doc b{display:block;font-family:Archivo,sans-serif;font-size:16.5px;font-weight:600;line-height:1.25}
.doc .kind{display:block;font-size:11px;font-weight:600;letter-spacing:.09em;text-transform:uppercase;
  color:var(--accent);margin:7px 0 9px}
.doc .d{display:block;font-size:14.5px;color:var(--ink-2);line-height:1.5}

footer{border-top:1px solid var(--line);padding:26px 0 60px;font-size:13.5px;color:var(--muted)}
footer p{max-width:90ch;margin:0}
footer b{color:var(--ink-2)}

@media (max-width:820px){
  .docs{grid-template-columns:1fr}
  .card{grid-template-columns:1fr;gap:14px}
  .wrap{padding:0 20px}
}
"""
    doc = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n" + HEAD_BASE + THEME_SCRIPT
        + '\n<title>WeYield Advisory Pack</title>\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Archivo:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">\n'
        "<style>" + css + NAV_CSS + "</style>\n</head>\n<body>\n"
        + nav_html("index") + "\n" + DEFS + body + "\n" + TOGGLE_SCRIPT + "\n</body>\n</html>\n"
    )
    io.open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(doc)


os.makedirs(OUT, exist_ok=True)
for _f in os.listdir(OUT):
    _p = os.path.join(OUT, _f)
    if os.path.isfile(_p) and (_f.endswith(".html") or _f.endswith(".json")):
        os.remove(_p)

titles = {}
for slug, srcfile, label, n, q in PAGES:
    titles[slug] = build_page(slug, srcfile, slug)
    print("built %-16s %s" % (slug, titles[slug]))
build_index(titles)
print("built index.html")

io.open(os.path.join(OUT, "vercel.json"), "w", encoding="utf-8").write(
    '{\n  "cleanUrls": true,\n  "trailingSlash": false\n}\n')
io.open(os.path.join(OUT, ".vercelignore"), "w", encoding="utf-8").write("*.py\n")
print("wrote vercel.json")
print("\nOUT:", OUT)
for f in sorted(os.listdir(OUT)):
    print("  %8d  %s" % (os.path.getsize(os.path.join(OUT, f)), f))
