# -*- coding: utf-8 -*-
"""WeYield — Building the AI-Native Business. McKinsey-grammar deck, python-pptx, shape-drawn exhibits."""
import re, sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

OUT = sys.argv[1] if len(sys.argv) > 1 else "WeYield - Building the AI-Native Business.pptx"

# ---------- palette ----------
NAVY = RGBColor(0x05, 0x1C, 0x2C)
BLUE = RGBColor(0x22, 0x51, 0xFF)
LBLUE = RGBColor(0x99, 0xB4, 0xFF)
PALE = RGBColor(0xE8, 0xEE, 0xFF)
INK = RGBColor(0x26, 0x26, 0x26)
GREY = RGBColor(0x7F, 0x7F, 0x7F)
MID = RGBColor(0xB3, 0xB3, 0xB3)
RULE = RGBColor(0xD9, 0xD9, 0xD9)
BG2 = RGBColor(0xF4, 0xF5, 0xF7)
WARN = RGBColor(0xB3, 0x66, 0x1A)
WARN_SOFT = RGBColor(0xF7, 0xE9, 0xDA)
OK = RGBColor(0x1D, 0x70, 0x49)
BAD = RGBColor(0xA8, 0x34, 0x1C)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xB5, 0x1D, 0x1D)
AMBER = RGBColor(0xB3, 0x6B, 0x00)
GREEN = RGBColor(0x1E, 0x7F, 0x4F)

SERIF = "Georgia"
SANS = "Arial"

W, H = 13.333, 7.5
ML, MR = 0.5, 0.5
TITLE_Y, TITLE_H, TITLE_W = 0.42, 1.0, 10.6
BODY_Y, BODY_B = 1.62, 6.75
SRC_Y = 6.95

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
BLANK = prs.slide_layouts[6]
page_no = [0]


# ---------- primitives ----------
def rect(slide, x, y, w, h, fill=None, line=None, line_w=0.75, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.shadow.inherit = False
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(line_w)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            s.adjustments[0] = 0.12
        except Exception:
            pass
    s.text_frame.text = ""
    return s


def hline(slide, x, y, w, color=RULE, weight=0.75):
    ln = slide.shapes.add_connector(1, Inches(x), Inches(y), Inches(x + w), Inches(y))
    ln.line.color.rgb = color; ln.line.width = Pt(weight)
    return ln


def vline(slide, x, y, h, color=RULE, weight=0.75):
    ln = slide.shapes.add_connector(1, Inches(x), Inches(y), Inches(x), Inches(y + h))
    ln.line.color.rgb = color; ln.line.width = Pt(weight)
    return ln


def _runs(p, text, size, color, bold=False, italic=False, font=SANS):
    """**bold** and *italic* mini-markup."""
    parts = re.split(r'(\*\*.+?\*\*|(?<!\*)\*(?!\*).+?(?<!\*)\*(?!\*))', text)
    for t in parts:
        if not t:
            continue
        b, it = bold, italic
        if t.startswith('**') and t.endswith('**'):
            t = t[2:-2]; b = True
        elif t.startswith('*') and t.endswith('*') and len(t) > 2:
            t = t[1:-1]; it = True
        r = p.add_run(); r.text = t
        r.font.size = Pt(size); r.font.bold = b; r.font.italic = it
        r.font.color.rgb = color; r.font.name = font


def set_bullet(p, char="•", indent_in=0.18, color=None):
    pPr = p._p.get_or_add_pPr()
    pPr.set('marL', str(int(Inches(indent_in))))
    pPr.set('indent', str(-int(Inches(indent_in))))
    for tag in ('a:buNone', 'a:buChar', 'a:buAutoNum', 'a:buClr', 'a:buFont'):
        e = pPr.find(qn(tag))
        if e is not None:
            pPr.remove(e)
    if color is not None:
        buClr = etree.SubElement(pPr, qn('a:buClr'))
        etree.SubElement(buClr, qn('a:srgbClr'), val='%02X%02X%02X' % (color[0], color[1], color[2]))
    buFont = etree.SubElement(pPr, qn('a:buFont'), typeface=SANS)
    etree.SubElement(pPr, qn('a:buChar'), char=char)


def text(slide, x, y, w, h, paras, size=11, color=INK, bold=False, italic=False, font=SANS,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space_after=4, line_spacing=None,
         bullets=False, bullet_char="•", margins=(0, 0, 0, 0), fill=None, line=None):
    """paras: str or list of str | (str, dict overrides)."""
    if fill is not None or line is not None:
        box = rect(slide, x, y, w, h, fill=fill, line=line)
        tf = box.text_frame
    else:
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = [Inches(m) for m in margins]
    tf.vertical_anchor = anchor
    if isinstance(paras, str):
        paras = [paras]
    first = True
    for item in paras:
        if isinstance(item, tuple):
            t, o = item
        else:
            t, o = item, {}
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = o.get('align', align)
        p.space_after = Pt(o.get('space_after', space_after))
        if o.get('space_before') is not None:
            p.space_before = Pt(o['space_before'])
        ls = o.get('line_spacing', line_spacing)
        if ls:
            p.line_spacing = ls
        _runs(p, t, o.get('size', size), o.get('color', color), o.get('bold', bold), o.get('italic', italic), o.get('font', font))
        if o.get('bullet', bullets):
            set_bullet(p, o.get('bullet_char', bullet_char), o.get('indent', 0.18), o.get('bullet_color'))
    return box


def cell_borders(cell, top=None, bottom=None, left=None, right=None):
    """Each side: None → no line; else (hex, pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):
        e = tcPr.find(qn(tag))
        if e is not None:
            tcPr.remove(e)
    order = [('a:lnL', left), ('a:lnR', right), ('a:lnT', top), ('a:lnB', bottom)]
    idx = 0
    for tag, spec in order:
        if spec is None:
            ln = etree.Element(qn(tag), w='0')
            etree.SubElement(ln, qn('a:noFill'))
        else:
            hexc, pt = spec
            ln = etree.Element(qn(tag), w=str(int(pt * 12700)), cap='flat', cmpd='sng', algn='ctr')
            sf = etree.SubElement(ln, qn('a:solidFill'))
            etree.SubElement(sf, qn('a:srgbClr'), val=hexc)
            etree.SubElement(ln, qn('a:prstDash'), val='solid')
        tcPr.insert(idx, ln); idx += 1


def table(slide, x, y, w, rows, col_w, size=9.5, header=True, row_h=0.36, header_fill=NAVY,
          header_color=WHITE, zebra=False, bold_first_col=False, valign=MSO_ANCHOR.TOP, pad=0.06,
          col_align=None, header_size=None, status_col=None, header_h=0.42):
    nrows, ncols = len(rows), len(rows[0])
    shp = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y), Inches(w), Inches(row_h * nrows))
    tbl = shp.table
    tblPr = tbl._tbl.tblPr
    sid = tblPr.find(qn('a:tableStyleId'))
    if sid is None:
        sid = etree.SubElement(tblPr, qn('a:tableStyleId'))
    sid.text = '{2D5ABB26-0587-4C30-8999-92F81FD0307C}'
    tblPr.set('firstRow', '0'); tblPr.set('bandRow', '0')
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Inches(cw)
    for r in range(nrows):
        tbl.rows[r].height = Inches(header_h if (header and r == 0) else row_h)
        for c in range(ncols):
            cell = tbl.cell(r, c)
            cell.margin_left = cell.margin_right = Inches(pad)
            cell.margin_top = Inches(0.045); cell.margin_bottom = Inches(0.045)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE if (header and r == 0) else valign
            val = rows[r][c]
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            if col_align and col_align[c]:
                p.alignment = col_align[c]
            is_hdr = header and r == 0
            if is_hdr:
                cell.fill.solid(); cell.fill.fore_color.rgb = header_fill
                _runs(p, str(val), header_size or size, header_color, bold=True)
                cell_borders(cell, bottom=('051C2C', 0.75))
            else:
                if zebra and r % 2 == 0:
                    cell.fill.solid(); cell.fill.fore_color.rgb = BG2
                else:
                    cell.fill.background()
                colr = INK
                b = bold_first_col and c == 0
                if status_col is not None and c == status_col:
                    v = str(val).upper()
                    if v.startswith('HELD') or v.startswith('COVERED'):
                        colr = GREEN
                    elif 'MISSING' in v or v.startswith('NOT'):
                        colr = RED
                    elif 'ONLY' in v:
                        colr = AMBER
                    elif 'UNKNOWN' in v:
                        colr = BLUE
                    else:
                        colr = INK
                    b = True
                _runs(p, str(val), size, colr, bold=b)
                cell_borders(cell, bottom=('D9D9D9', 0.75))
    return shp


# ---------- chrome ----------
def new_slide(title, tracker=None, sticker=None, source=None):
    s = prs.slides.add_slide(BLANK)
    page_no[0] += 1
    text(s, ML, TITLE_Y, TITLE_W, TITLE_H, title, size=20, color=NAVY, font=SERIF, anchor=MSO_ANCHOR.TOP,
         line_spacing=1.05, space_after=0)
    hline(s, ML, 1.47, W - ML - MR, color=NAVY, weight=0.75)
    if tracker:
        text(s, 9.9, 0.2, 2.93, 0.25, tracker.upper(), size=7.5, color=GREY, align=PP_ALIGN.RIGHT)
    if sticker:
        b = rect(s, 11.53, 0.52, 1.3, 0.27, fill=None, line=NAVY, line_w=0.75, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        tf = b.text_frame; tf.margin_left = tf.margin_right = Inches(0.02); tf.margin_top = tf.margin_bottom = Inches(0)
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        _runs(p, sticker.upper(), 7.5, NAVY, bold=True)
    if source:
        text(s, ML, SRC_Y, 10.8, 0.4, source, size=7.5, color=GREY, line_spacing=1.0, space_after=0)
    text(s, 12.0, SRC_Y + 0.02, 0.83, 0.25, str(page_no[0]), size=8.5, color=GREY, align=PP_ALIGN.RIGHT)
    hline(s, ML, SRC_Y - 0.08, W - ML - MR, color=RULE, weight=0.5)
    return s


def callout(slide, x, y, w, h, title, body, fill=PALE, accent=BLUE, title_size=10, body_size=10):
    rect(slide, x, y, w, h, fill=fill)
    rect(slide, x, y, 0.06, h, fill=accent)
    paras = []
    if title:
        paras.append((title, {'bold': True, 'size': title_size, 'color': NAVY, 'space_after': 5}))
    if isinstance(body, str):
        body = [body]
    for b in body:
        paras.append((b, {'size': body_size, 'color': INK, 'space_after': 5}))
    text(slide, x + 0.2, y + 0.14, w - 0.34, h - 0.24, paras, line_spacing=1.1)


def kpi(slide, x, y, w, h, value, label, sub=None, accent=NAVY):
    rect(slide, x, y, w, h, fill=WHITE, line=RULE)
    rect(slide, x, y, w, 0.05, fill=accent)
    text(slide, x + 0.15, y + 0.2, w - 0.3, 0.5, value, size=22, color=NAVY, font=SERIF, space_after=0)
    paras = [(label, {'size': 9, 'color': INK, 'bold': True, 'space_after': 1})]
    if sub:
        paras.append((sub, {'size': 8, 'color': GREY}))
    text(slide, x + 0.15, y + 0.78, w - 0.3, h - 0.85, paras, line_spacing=1.05)


def hbars(slide, x, y, w, items, max_val, label_w=2.6, bar_h=0.34, gap=0.2, fmt=lambda v: f"{v}",
          value_w=1.1, label_size=10, threshold=None, threshold_label=None, label_color=INK):
    """items: (label, value, color, optional value-label override)."""
    bar_x = x + label_w + 0.1
    bar_w_max = w - label_w - 0.1 - value_w
    for i, it in enumerate(items):
        label, val, col = it[0], it[1], it[2]
        vlabel = it[3] if len(it) > 3 else fmt(val)
        yy = y + i * (bar_h + gap)
        text(slide, x, yy, label_w, bar_h, label, size=label_size, color=label_color, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
        bw = max(0.02, bar_w_max * val / max_val)
        rect(slide, bar_x, yy, bw, bar_h, fill=col)
        text(slide, bar_x + bw + 0.08, yy, value_w + 0.5, bar_h, vlabel, size=label_size, color=NAVY, bold=True,
             anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    total_h = len(items) * (bar_h + gap) - gap
    vline(slide, bar_x, y - 0.05, total_h + 0.1, color=NAVY, weight=0.75)
    if threshold is not None:
        tx = bar_x + bar_w_max * threshold / max_val
        ln = slide.shapes.add_connector(1, Inches(tx), Inches(y - 0.12), Inches(tx), Inches(y + total_h + 0.12))
        ln.line.color.rgb = RED; ln.line.width = Pt(1.25); ln.line.dash_style = 4
        if threshold_label:
            text(slide, tx - 1.0, y + total_h + 0.16, 2.0, 0.3, threshold_label, size=8.5, color=RED, align=PP_ALIGN.CENTER, bold=True)
    return bar_x, bar_w_max


def vcols(slide, x, y, w, h, items, max_val, fmt=lambda v: f"{v}", col_w=None, top_labels=None,
          label_size=10, value_size=12, base_label=None):
    """items: (label, value, color). Draws baseline + columns + value labels above + category labels below."""
    n = len(items)
    slot = w / n
    cw = col_w or slot * 0.52
    base_y = y + h - 0.5
    plot_h = h - 0.5 - 0.45
    hline(slide, x, base_y, w, color=NAVY, weight=0.75)
    for i, (label, val, col) in enumerate(items):
        cx = x + slot * i + (slot - cw) / 2
        ch = plot_h * val / max_val
        rect(slide, cx, base_y - ch, cw, ch, fill=col)
        text(slide, cx - 0.3, base_y - ch - 0.36, cw + 0.6, 0.32, fmt(val), size=value_size, color=NAVY, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM, space_after=0)
        if top_labels and top_labels[i]:
            text(slide, cx - 0.3, base_y - ch - 0.66, cw + 0.6, 0.3, top_labels[i], size=9, color=BLUE, bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM, space_after=0)
        text(slide, x + slot * i, base_y + 0.06, slot, 0.44, label, size=label_size, color=INK, align=PP_ALIGN.CENTER,
             line_spacing=1.0, space_after=0)


# =====================================================================
# SLIDES
# =====================================================================



# ---------- 1. Cover ----------
s = prs.slides.add_slide(BLANK); page_no[0] += 1
rect(s, 0, 0, W, H, fill=NAVY)
rect(s, ML, 1.5, 0.9, 0.06, fill=BLUE)
text(s, ML, 1.72, 10.5, 1.9, ["Building the", "AI-native WeYield"], size=44, color=WHITE, font=SERIF, line_spacing=1.0, space_after=0)
text(s, ML, 3.66, 9.8, 0.6, "Version 2 — rewritten after our conversation of 13 September",
     size=16, color=BLUE, line_spacing=1.15)
text(s, ML, 4.16, 9.8, 0.9, "You have already built the hard half. This is about the half that is missing — and about the car, not the rate.",
     size=15, color=LBLUE, line_spacing=1.2)
text(s, ML, 5.25, 8, 0.9, [("Strategic recommendation", {'bold': True, 'size': 12, 'color': WHITE, 'space_after': 3}),
                            ("Prepared for Emmanuel Scuto, Chief Executive Officer", {'size': 11, 'color': LBLUE, 'space_after': 3}),
                            ("Ram Badrinathan  ·  14 September 2026", {'size': 11, 'color': LBLUE})])
hline(s, ML, 6.7, W - ML - MR, color=RGBColor(0x2A, 0x3F, 0x52), weight=0.5)
text(s, ML, 6.8, 8, 0.3, "PRELIMINARY — FOR DISCUSSION  ·  CONFIDENTIAL", size=8, color=LBLUE)
text(s, 8.5, 6.8, 4.3, 0.3, "Corrected against Emmanuel's own account, 13 Sep. Still not verified against company records.",
     size=8, color=LBLUE, align=PP_ALIGN.RIGHT)

# ---------- 2. What changed ----------
s = new_slide("What version 1 got wrong — corrected from your own account",
              tracker="Version 2",
              source="Source: conversation with Emmanuel Scuto, 13 September 2026. Version 1 was built from Olivier Jager's briefing and weyield.io alone; each row below replaces an inference with something you said.")
table(s, ML, BODY_Y + 0.05, W - ML - MR, [
    ["", "Version 1 assumed", "You said", "What it changes"],
    ["**The agent**", "That an AI layer had to be built from scratch", "Christian has trained a 3B model on three years of your own recorded consultant calls. Self-hosted, no token cost, 95–97%, already with customers.", "**The whole posture.** This deck is now about completing it, not starting it."],
    ["**Geography**", "Europe-centric, with a long tail on islands and North Africa", "“No, no — around the world, all of the world.”", "The low-emission-zone analysis is Europe-only and cannot carry the residual argument on its own"],
    ["**Market size**", "600 to 1,000 operators", "“100 plus out of the market of 1,000”", "Penetration is ~10%, and the ceiling arithmetic moves"],
    ["**Profitability**", "EBITDA flat to contracting", "“More or less we are **not making money over the last 10 years**.”", "This is not a margin problem to optimise. It is a model that has never paid."],
    ["**Exit horizon**", "Two to three years, sale to a third party", "Five to six years, handing to your two C-levels — or reselling with them as shareholders", "Changes what the plan is optimising for. **This contradicts Olivier's note — worth reconciling.**"],
    ["**The buyer**", "An operator with a tool budget", "“The last industry in travel accessible to you and I.” Craftsmen. One customer with 15 companies still updates rates with an Excel macro.", "The single most important design constraint, and version 1 barely registered it"],
], col_w=[1.35, 2.6, 4.6, 3.78], size=9, row_h=0.72, header_size=9)

# ---------- 3. You already built the hard half ----------
s = new_slide("You have already built the part everyone else finds hard",
              tracker="1 · Where you actually are",
              source="Source: Emmanuel Scuto, 13 September 2026. Model size, quality figure and deployment described by him; not independently verified.")
callout(s, ML, BODY_Y + 0.05, 6.3, 2.7, "What Christian built in three months",
        ["Three years of **every consultant–customer conversation**, recorded with consent. Turned into question-and-answer pairs, and used to fine-tune a **3-billion-parameter open model** — self-hosted, on your own infrastructure.",
         "**“We don't buy any tokens because it's on our side. We do what we want.”**",
         "The output: a **daily summary telling the customer what to do today**, across horizons. Quality at **95–97%** of how your own analysts would have written it. Already in customer testing."], body_size=10.5)
rect(s, ML, BODY_Y + 2.95, 6.3, 2.05, fill=NAVY)
text(s, ML + 0.22, BODY_Y + 3.1, 5.9, 0.4, "WHY THIS IS RARE", size=9, color=LBLUE, bold=True)
text(s, ML + 0.22, BODY_Y + 3.42, 5.9, 1.5,
     "Almost nobody has a **proprietary training corpus** in a vertical this narrow. Three years of expert conversation about car rental revenue management does not exist anywhere else, and cannot be bought. A generic model gave you hallucination; yours gives you 95–97% — that gap **is** the corpus.",
     size=10.5, color=WHITE, line_spacing=1.15, space_after=0)
text(s, 7.0, BODY_Y, 5.83, 0.3, "What it means for this deck", size=11, color=NAVY, bold=True)
table(s, 7.0, BODY_Y + 0.4, 5.83, [
    ["Version 1 said", "Version 2 says"],
    ["Build a weekly brief in a coach's voice", "**You have it.** Make it defensible and make it sell."],
    ["Ship the engine first, it takes eight weeks", "The engine is largely running. **Eight weeks is now about the missing layer**, not the model."],
    ["Adopt a frontier model on EU infrastructure", "Keep yours for the daily summary. Reach for a frontier model only where yours cannot go — see slide 16."],
    ["The methodology has to be written down", "It already is — **inside the weights.** The risk is that it is *only* there."],
], col_w=[2.55, 3.28], size=9.5, row_h=0.78)
callout(s, 7.0, BODY_Y + 3.75, 5.83, 1.25, None,
        ["The uncomfortable implication: if the method now lives in a fine-tune nobody can read, **you cannot audit it, price it, or defend a wrong answer.** That is what the next slides are about."],
        fill=BG2, accent=NAVY, body_size=10)

# ---------- 4. Executive summary ----------
s = new_slide("Executive summary — the product is right, the object is wrong, and the missing layer is trust",
              tracker="Executive summary",
              source="Source: Emmanuel Scuto, 13 September 2026; Olivier Jager's strategic review, 10 September 2026; weyield.io. Financial and market figures as reported by the company; nothing verified against records.")
pts = [
    ("**You have a genuine asset and a model that has never paid.** Ten years without making money, on a product the market calls a worldwide reference. That combination is not a pricing problem — it is a problem of what is being sold.", {}),
    ("**Your agent is real, and it is 3–5% wrong.** At 95–97% the model is good enough to impress and not good enough to sell on outcome. What is missing is not intelligence — it is a **deterministic layer around it**: computed facts, a rules engine, a verifier, and euro values on every recommendation.", {}),
    ("**Your customer is a craftsman, not an analyst.** Excel macros, no abstraction, “the last industry in travel accessible to you and I.” This kills the dashboard, validates email, and makes the coach more important, not less.", {}),
    ("**The profit is in the car, and you have never touched it.** Sixty to seventy per cent of your customers' cost is the vehicle itself. You optimise the rate. Nobody sells the buy-and-sell decision to this segment.", {}),
    ("**Two clocks are running.** The counter — the last place your customers make money — is being disinterme­diated. And OEMs are entering rental with unlimited capacity and the one thing your customers cannot offer: the car you actually booked.", {}),
    ("**Build is no longer the constraint; distribution is.** The friction of making software has gone. Minimum viable product has become **minimum viable distribution** — and that, not engineering, is what the next twelve months should be organised around.", {}),
]
yy = BODY_Y + 0.05
for i, (t, o) in enumerate(pts):
    rect(s, ML, yy + 0.04, 0.34, 0.34, fill=NAVY)
    text(s, ML, yy + 0.04, 0.34, 0.34, str(i + 1), size=11, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(s, ML + 0.5, yy, W - ML - MR - 0.5, 0.8, t, size=11, color=INK, line_spacing=1.12, space_after=0)
    yy += 0.84

# ---------- 5. Where WeYield stands ----------
s = new_slide("A worldwide reference in its category that has not made money in ten years",
              tracker="1 · Where you actually are",
              source="Source: Emmanuel Scuto, 13 September 2026, except where marked. Figures as stated by the company; not verified against records.")
tiles = [
    ("2012", "Founded", "Emmanuel's fourteenth year"),
    ("100+", "Customers", "of a workable market of ~1,000"),
    ("~10%", "Penetration", "and the base is worldwide"),
    ("10 yrs", "Without profit", "“more or less we are not making money”"),
    ("9", "People", "Christian CTO, PhD maths and CS"),
    ("1 + 1", "In sales", "one hire 10 months ago, 8 to ramp"),
    ("5–6 yrs", "Exit horizon", "to the two C-levels, or resale with them"),
    ("3 yrs", "Of recorded calls", "the training corpus, and the moat"),
]
tx, ty, tw, th, tg = ML, BODY_Y + 0.05, 1.98, 1.42, 0.16
for i, (v, l, sub) in enumerate(tiles):
    kpi(s, tx + (i % 4) * (tw + tg), ty + (i // 4) * (th + tg), tw, th, v, l, sub,
        accent=(BLUE if i in (3, 7) else NAVY))
callout(s, 9.2, BODY_Y + 0.05, 3.63, 2.55, "Emmanuel's own diagnosis",
        ["“We are a **product mindset type of team** who love developing features and we believe improving the service and avoiding the attrition of our customers — but as a matter of fact **we don't make any penny**. So there is a trick somewhere.”",
         "“The cost of delivering this service is expensive… we **didn't find the formula to turn lead into gold**.”"], body_size=9.5)
callout(s, 9.2, BODY_Y + 2.75, 3.63, 2.25, "The differentiation that costs the money",
        ["Regain, Margin Fuel and RateHighway tackle **rate updating**. WeYield chose instead to build **the skill of the person** — to teach them to read the market and decide.",
         "That is why it is a reference. It is also why it is expensive to deliver. **Both facts have the same cause.**"],
        fill=BG2, accent=GREY, body_size=9.5)

# ---------- 6. The customer ----------
s = new_slide("The design constraint version 1 missed: your customer is a craftsman, not an analyst",
              tracker="2 · What the market actually is",
              source="Source: Emmanuel Scuto, 13 September 2026 — all quotations are his. This slide is the reason several version-1 recommendations have been withdrawn.")
callout(s, ML, BODY_Y + 0.05, 6.1, 2.35, "Who actually buys",
        ["“**The last industry in travel accessible to you and I.** You have $100,000, you can buy ten cars and become a car rental company. In the US some people get their pension at once, buy fifty cars, and become a car rental company.”",
         "“It is **not an engineer type of business**. People don't have a high level of abstraction… good entrepreneurs, smart, but not with this techno mindset. **They are more followers.** Managing a bit like a craftsman opening his bakery.”"], body_size=10)
rect(s, ML, BODY_Y + 2.6, 6.1, 2.4, fill=BG2)
text(s, ML + 0.22, BODY_Y + 2.75, 5.7, 0.3, "TWO FACTS THAT SHOULD DECIDE THE ROADMAP", size=9, color=WARN, bold=True)
text(s, ML + 0.22, BODY_Y + 3.1, 5.7, 1.8, [
    ("A customer running **15 car rental companies worldwide** still updates rates with **a macro in Excel**.", {'space_after': 8}),
    ("Your **number-one customer** reverted to **VBA macros** last summer when a competitor's rate updater failed.", {'space_after': 8}),
    ("These are not laggards. They are the market.", {'italic': True, 'color': GREY}),
], size=10.5, line_spacing=1.15)
text(s, 6.9, BODY_Y, 5.93, 0.3, "What this changes", size=11, color=NAVY, bold=True)
table(s, 6.9, BODY_Y + 0.4, 5.93, [
    ["Decision", "Version 2 position"],
    ["**A dashboard or portal**", "No. It will not be opened. Email, and the language they read."],
    ["**Self-serve sign-up**", "Withdrawn as designed. This buyer does not onboard themselves — but an **agent that reads their messy export** is exactly right."],
    ["**The coach**", "More important, not less. The human is what makes the output trusted by someone who cannot audit it."],
    ["**Explainability**", "Not a feature for regulators. It is how a craftsman decides whether to act."],
    ["**Where AI actually lands**", "Inside *your* cost of delivery first — not inside their workflow. They will not adopt what they cannot picture."],
], col_w=[1.85, 4.08], size=9.5, row_h=0.68)

# ---------- 7. Five levers ----------
s = new_slide("Sixty to seventy per cent of your customer's cost is the car — and that is the part you do not touch",
              tracker="2 · What the market actually is",
              source="Cost share and operational examples: Emmanuel Scuto, 13 September 2026. Status column inferred from weyield.io and confirmed in conversation. ACRISS codes define the substitution ladder.")
callout(s, ML, BODY_Y + 0.05, 3.5, 4.95, "In his words",
        ["“What drives most of the car rental activity is **the operations**. Moving cars, delivering cars, problems with staff, clients… a car expected back tomorrow at Charles de Gaulle comes back Monday somewhere else, and it is **not ready to re-rent** because it is half broken.”",
         "“Between **60% and 70% of cost is related to the car itself**. And we are touching only **this** proportion.”",
         "“**Everything else is a pain, is extremely costing** — and they have more and more cost.”"], body_size=10)
table(s, 4.25, BODY_Y + 0.05, 8.58, [
    ["Lever", "The decision", "Who makes it today", "WeYield today"],
    ["**Price**", "Rate by car group, channel, booking window, length of rental", "Revenue manager — your user", "Covered"],
    ["**Move**", "Transfer units between stations; recover a car that came back in the wrong place, damaged", "Operations, by instinct, under daily pressure", "Analytics only — no redistribution recommended"],
    ["**Substitute**", "Walk the customer up the ACRISS ladder", "Counter staff, ad hoc", "Not covered"],
    ["**Buy**", "How many of each group, when, at what price — and what they will be worth", "Owner, annually, by gut", "Demand-side only — no cost or residual view"],
    ["**Sell**", "When to de-fleet each cohort — the decision that sets the year", "Owner, by gut or by lease expiry", "Demand-side only — no residual view"],
], col_w=[1.1, 3.05, 2.55, 1.88], size=9.5, row_h=0.66, status_col=3)

# ---------- 8. Profit equation ----------
s = new_slide("The year is decided on the residual — and you have already started testing this with customers",
              tracker="3 · Where the profit is", sticker="Illustrative",
              source="Assumptions: 1,000-vehicle operator; €700 revenue per unit per month; ~4% net margin; €15K average disposal value; 24-month hold. Quotations: Emmanuel Scuto, 13 September 2026. Hertz Tesla write-down per public filings 2023–24.")
eq_y = BODY_Y + 0.15
def eqbox(x, w, label, sub, fill, color, subcolor):
    rect(s, x, eq_y, w, 0.95, fill=fill)
    text(s, x + 0.1, eq_y + 0.1, w - 0.2, 0.45, label, size=11, color=color, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(s, x + 0.1, eq_y + 0.55, w - 0.2, 0.35, sub, size=8.5, color=subcolor, align=PP_ALIGN.CENTER, space_after=0, line_spacing=1.0)
def op(x, ch):
    text(s, x, eq_y, 0.4, 0.95, ch, size=20, color=NAVY, font=SERIF, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
eqbox(ML, 1.5, "Profit", "the operator's annual result", NAVY, WHITE, LBLUE)
op(2.0, "=")
eqbox(2.4, 3.4, "Rental revenue − Operating cost", "Revenue management · WeYield today", RULE, INK, GREY)
op(5.8, "+")
eqbox(6.2, 3.9, "Residual realised − Depreciation booked", "60–70% of their cost sits here · unserved", BLUE, WHITE, PALE)
op(10.1, "−")
eqbox(10.5, 2.33, "Holding cost", "financing, insurance, storage", RULE, INK, GREY)
text(s, ML, BODY_Y + 1.4, 7.2, 0.3, "Sizing the second bracket for a 1,000-vehicle operator, €K per year", size=11, color=NAVY, bold=True)
hbars(s, ML, BODY_Y + 1.9, 7.2, [
    ("Annual net profit at 4% margin", 336, MID, "€336K"),
    ("Value of +1% residual realisation — low", 75, LBLUE, "€75K  (22% of profit)"),
    ("Value of +1% residual realisation — high", 150, BLUE, "€150K  (45% of profit)"),
], max_val=400, label_w=3.1, bar_h=0.42, gap=0.34, value_w=1.9, label_size=9.5)
callout(s, 8.1, BODY_Y + 1.45, 4.73, 1.9, "You are already validating this",
        ["“The thing with the car was a **mind blower** for me. I was discussing over the last two days with **some of my customers** and I will continue.”",
         "“**That's something I never touched — this car issue.**”"], body_size=10)
callout(s, 8.1, BODY_Y + 3.5, 4.73, 1.5, "And Olivier's provocation goes further",
        ["“Eventually **the owner could get rid of the general manager.** What if the company could run without the GM?” If the decisions come from the system, the org chart changes — and so does what you can charge."],
        fill=BG2, accent=GREY, body_size=9.5)

# ---------- 9. Why now ----------
s = new_slide("Six forces, and the two most violent are ones you named",
              tracker="3 · Where the profit is",
              source="Forces 1 and 2 and the distribution point: Emmanuel Scuto, 13 September 2026. Others: industry reporting on OEM repurchase programmes post-2021, Hertz/Tesla write-downs, Indicata and Autovista data products, RateHighway's expandable pricing framework.")
conds = [
    ("Chinese EVs are being built inside European factories",
     "European manufacturers are renting factory capacity to Chinese makers, who then reach the European market with **no import tariff — because it is no longer an import**. “The pressure on car will be more and more.” A sustained downward force on new prices, and therefore on every residual behind them.", True),
    ("OEMs have started renting cars themselves",
     "Unlimited capacity. Located in the suburbs, where people actually live. And the one thing your customers cannot match: **rent an Audi, get an Audi** — not “this car or similar”. Not at airports or stations yet. That is the only thing holding.", True),
    ("The risk moved to the operator",
     "OEM buyback and repurchase contracted after 2021. The long tail now carries residual exposure it never held — and mostly cannot see on its own reporting.", False),
    ("The risk became unforecastable by instinct",
     "EV collapse and diesel access rules destroyed the intuitions that used to substitute for a model.", False),
    ("The missing input became purchasable",
     "Used-vehicle intelligence is now an API — Indicata, Autovista, BCA, Manheim. Five years ago this was a licensing project.", False),
    ("Standing still stopped being safe",
     "RateHighway is building a framework that hosts third-party pricing engines. A pricing engine inside someone else's store is a commodity.", False),
]
cw_, cg_ = 1.96, 0.1
for i, (hd, body, mine) in enumerate(conds):
    cx = ML + i * (cw_ + cg_)
    rect(s, cx, BODY_Y + 0.05, cw_, 0.78, fill=(BLUE if mine else NAVY))
    text(s, cx + 0.1, BODY_Y + 0.05, 0.4, 0.78, str(i + 1), size=19, color=WHITE, font=SERIF, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(s, cx + 0.48, BODY_Y + 0.05, cw_ - 0.58, 0.78, hd, size=9.5, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05, space_after=0)
    rect(s, cx, BODY_Y + 0.83, cw_, 3.2, fill=(PALE if mine else BG2))
    text(s, cx + 0.13, BODY_Y + 0.96, cw_ - 0.26, 3.0, body, size=9, color=INK, line_spacing=1.1)
    if mine:
        text(s, cx, BODY_Y + 4.08, cw_, 0.25, "YOUR OBSERVATION", size=7.5, color=BLUE, bold=True, align=PP_ALIGN.CENTER, space_after=0)
text(s, ML, BODY_Y + 4.42, W - ML - MR, 0.5,
     "Both of the forces you named point at the same place: the value of the car. Neither points at the rate.",
     size=13, color=NAVY, font=SERIF, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 10. The counter disappears ----------
s = new_slide("The last place your customers make money is being engineered away — which puts a clock on one of the five moves",
              tracker="3 · Where the profit is",
              source="Source: Emmanuel Scuto, 13 September 2026. Ancillary share and margin are industry norms, not WeYield figures — confirm before quoting to a customer.")
text(s, ML, BODY_Y + 0.02, 12, 0.3, "The rental journey, and where the margin used to sit", size=11, color=NAVY, bold=True)
stages = [
    ("Booking", "OTA or direct", BG2, False),
    ("Pre-arrival", "48 hours out — email, app", PALE, True),
    ("The counter", "upgrade, waiver, extras", WARN_SOFT if False else BG2, False),
    ("The rental", "you have no control", BG2, False),
    ("Return", "damage, fuel, delay", BG2, False),
]
sw_, sg_ = 2.4, 0.12
for i, (hd, sub, fill, keep) in enumerate(stages):
    sx = ML + i * (sw_ + sg_)
    rect(s, sx, BODY_Y + 0.4, sw_, 0.95, fill=(BLUE if keep else fill))
    text(s, sx + 0.14, BODY_Y + 0.52, sw_ - 0.28, 0.4, hd, size=13, color=(WHITE if keep else INK), bold=True, space_after=0)
    text(s, sx + 0.14, BODY_Y + 0.9, sw_ - 0.28, 0.4, sub, size=10, color=(PALE if keep else GREY), space_after=0)
    if i < 4:
        text(s, sx + sw_ - 0.02, BODY_Y + 0.62, sg_ + 0.1, 0.5, "›", size=15, color=GREY, align=PP_ALIGN.CENTER, space_after=0)
rect(s, ML + 2 * (sw_ + sg_), BODY_Y + 1.42, sw_, 0.3, fill=BAD)
text(s, ML + 2 * (sw_ + sg_), BODY_Y + 1.42, sw_, 0.3, "BEING REMOVED", size=9, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
rect(s, ML + 1 * (sw_ + sg_), BODY_Y + 1.42, sw_, 0.3, fill=BLUE)
text(s, ML + 1 * (sw_ + sg_), BODY_Y + 1.42, sw_, 0.3, "WHERE IT GOES", size=9, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
callout(s, ML, BODY_Y + 1.95, 6.1, 1.55, "What you said",
        ["“They want to go **directly from the reservation to the rental** with everything electronic. No queue, no paper check. *Mr Ram, we have checked your papers, go to parking lot 15 and get your key.*”",
         "“**The last part of the equation where they were able to make money — the counter sales — will eventually be disrupted pretty soon.**”"], body_size=9.5)
callout(s, 6.72, BODY_Y + 1.95, 6.11, 1.55, "What it does to the plan",
        ["Ancillaries are a quarter to a third of revenue at 80–90% margin. Version 1 proposed pricing them **at the counter and before arrival**. The counter half now has a shelf life.",
         "**The pre-arrival offer becomes the whole product** — and it is the half that needs no counter integration, so this is a simplification, not a loss."],
        fill=BG2, accent=BLUE, body_size=9.5)
rect(s, ML, BODY_Y + 3.65, W - ML - MR, 0.9, fill=NAVY)
text(s, ML + 0.25, BODY_Y + 3.65, W - ML - MR - 0.5, 0.9,
     "**And the same disintermediation is a reason the fleet product matters more.** If the counter margin goes and the OTA margin is already subsidised away, the operator's profit collapses onto exactly one thing: what the car was bought for and what it sells for. That is the bracket nobody serves.",
     size=11, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.15, space_after=0)

# ---------- 11. Recommendation ----------
s = new_slide("Recommendation — finish what Christian started, then change the object and the buyer",
              tracker="4 · The recommendation",
              source="Note: the three changes are sequenced, not parallel. Change 0 is new in version 2 and comes before everything, because the asset already exists and is not yet defensible or saleable.")
cols3 = [
    ("0", "Complete the agent", "A 3B fine-tune at 95–97%, unaudited", "The same model wrapped in a deterministic layer", "Computed facts, a coach-owned rules engine, a verifier that drops any sentence whose numbers do not check, euro values, and accept/reject telemetry. **This is eight weeks and it is the whole difference between impressive and sellable.**", OK),
    ("1", "Change the object", "The rate — one lever of five", "The fleet plan, and then the operation", "Sixty to seventy per cent of their cost is the car. You said it yourself: you have to *enter into* the operation, and every decision should come from your brain.", NAVY),
    ("2", "Change the buyer", "The revenue manager", "The owner — who has a P&L", "Your site already names the CEO as an audience and gives him nothing to read. The fleet P&L is that artefact. Owners have a profit and loss; clerks have a tool budget.", BLUE),
]
cw3, cg3 = 3.98, 0.2
for i, (n, hd, frm, to, why, col) in enumerate(cols3):
    cx = ML + i * (cw3 + cg3)
    rect(s, cx, BODY_Y + 0.05, cw3, 0.75, fill=col)
    text(s, cx + 0.15, BODY_Y + 0.05, 0.6, 0.75, n, size=26, color=WHITE, font=SERIF, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(s, cx + 0.75, BODY_Y + 0.05, cw3 - 0.9, 0.75, hd, size=14, color=WHITE, font=SERIF, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    rect(s, cx, BODY_Y + 0.8, cw3, 3.55, fill=BG2)
    text(s, cx + 0.2, BODY_Y + 0.95, cw3 - 0.4, 0.3, "FROM", size=8, color=GREY, bold=True, space_after=0)
    text(s, cx + 0.2, BODY_Y + 1.18, cw3 - 0.4, 0.62, frm, size=11, color=INK, line_spacing=1.05, space_after=0)
    text(s, cx + 0.2, BODY_Y + 1.85, cw3 - 0.4, 0.3, "TO", size=8, color=col, bold=True, space_after=0)
    text(s, cx + 0.2, BODY_Y + 2.08, cw3 - 0.4, 0.75, to, size=12, color=NAVY, bold=True, line_spacing=1.05, space_after=0)
    hline(s, cx + 0.2, BODY_Y + 2.92, cw3 - 0.4, color=RULE)
    text(s, cx + 0.2, BODY_Y + 3.02, cw3 - 0.4, 1.3, why, size=9.5, color=INK, line_spacing=1.1, space_after=0)
rect(s, ML, BODY_Y + 4.5, W - ML - MR, 0.5, fill=NAVY)
text(s, ML + 0.2, BODY_Y + 4.5, W - ML - MR - 0.4, 0.5,
     "Version 1 put “change the cost to serve” third. It is now first and renumbered zero — because you have already paid most of that cost, and the return on finishing it is higher than starting anything new.",
     size=10.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, space_after=0)

# ---------- 12. What is missing from the agent ----------
s = new_slide("What is missing is not intelligence. It is everything that makes an answer defensible.",
              tracker="4 · The recommendation",
              source="Note: 95–97% accuracy means three to five answers in a hundred are wrong. For a daily recommendation across 100+ accounts that is several wrong answers every week, and you cannot currently tell which ones.")
text(s, ML, BODY_Y, 12, 0.3, "The pipeline you have, and the four pieces around it", size=11, color=NAVY, bold=True)
have = [("Your data", "PH · MR · RH", False), ("Christian's 3B model", "fine-tuned on 3 years of calls", True), ("A daily summary", "in customer testing", False)]
hx = ML
for i, (hd, sub, mine) in enumerate(have):
    rect(s, hx, BODY_Y + 0.4, 2.55, 0.85, fill=(OK if mine else RULE))
    text(s, hx + 0.14, BODY_Y + 0.5, 2.3, 0.4, hd, size=12, color=(WHITE if mine else INK), bold=True, space_after=0)
    text(s, hx + 0.14, BODY_Y + 0.86, 2.3, 0.35, sub, size=9, color=(PALE if mine else GREY), space_after=0)
    if i < 2:
        text(s, hx + 2.55, BODY_Y + 0.55, 0.35, 0.5, "›", size=16, color=GREY, align=PP_ALIGN.CENTER, space_after=0)
    hx += 2.9
text(s, ML, BODY_Y + 1.32, 8.0, 0.25, "WHAT YOU HAVE", size=9, color=OK, bold=True)
missing = [
    ("A facts layer", "Every figure computed deterministically before the model sees it, with an ID and a link. The model writes; it never calculates.", "Removes the arithmetic hallucination entirely — the class of error that embarrasses you in front of a customer."),
    ("A rules engine", "The actions the model may propose come from a table the coach owns and edits — not from the weights. Ten rules to start, one a week after.", "Makes the method **visible and editable again**. Right now it is locked inside a fine-tune nobody can read."),
    ("A verifier", "Every number in every sentence matched back to a computed fact before send. No match, the sentence is dropped. No exceptions.", "This is what turns 95–97% into something you can put a price on. **It is the single highest-value piece of engineering on this page.**"),
    ("Accept / reject telemetry", "Log what was recommended, what the customer did, and what happened at T+7 and T+28.", "The evidence base for outcome pricing — and it **cannot be backfilled**. Every week without it is a week of history that never exists."),
]
mx = ML
for hd, what, why in missing:
    rect(s, mx, BODY_Y + 1.72, 3.03, 3.1, fill=BG2)
    rect(s, mx, BODY_Y + 1.72, 3.03, 0.06, fill=BLUE)
    text(s, mx + 0.16, BODY_Y + 1.88, 2.71, 0.35, hd, size=13, color=NAVY, bold=True, space_after=0)
    text(s, mx + 0.16, BODY_Y + 2.28, 2.71, 1.25, what, size=9.5, color=INK, line_spacing=1.12, space_after=0)
    hline(s, mx + 0.16, BODY_Y + 3.55, 2.71, color=RULE)
    text(s, mx + 0.16, BODY_Y + 3.65, 2.71, 1.05, why, size=9.5, color=BLUE, line_spacing=1.12, space_after=0)
    mx += 3.19
text(s, ML, BODY_Y + 4.92, W - ML - MR, 0.3, "MISSING — AND ALL FOUR ARE CODE, NOT MODEL WORK", size=9, color=BLUE, bold=True)

# ---------- 13. Your model, and when to reach for another ----------
s = new_slide("Keep your model. Reach for a frontier model only where yours structurally cannot go.",
              tracker="4 · The recommendation",
              source="Note: version 1 recommended a frontier model on EU infrastructure without knowing a fine-tune existed. That recommendation is withdrawn for the daily summary and narrowed to the four cases on the right.")
callout(s, ML, BODY_Y + 0.05, 6.1, 2.65, "Why your fine-tune is the right default",
        ["**Zero marginal cost.** No token bill, so cadence and volume are free decisions rather than budget decisions. This is a real strategic advantage and version 1 missed it.",
         "**Data sovereignty.** French company, worldwide customers, no third-party processor in the path. The DPA conversation is one page.",
         "**It knows things no frontier model does** — three years of how your own consultants actually reason about this market."], body_size=10)
callout(s, ML, BODY_Y + 2.9, 6.1, 2.1, "And where it will struggle",
        ["A 3B model is strong at the pattern it was trained on and weak outside it: **multilingual nuance across a worldwide base**, long chains of reasoning, tool use and agentic loops, and anything it has never seen. It will also be **confidently wrong** in exactly those cases."],
        fill=BG2, accent=WARN, body_size=10)
table(s, 6.9, BODY_Y + 0.05, 5.93, [
    ["Task", "Which model"],
    ["**The daily summary** — the thing it was trained for", "**Yours.** Do not change it."],
    ["**Writing to a customer in their own language** across a worldwide base", "Frontier. Multilingual quality is where a 3B model shows its size."],
    ["**The reply loop** — a customer asks *why*, and it must reason over the facts", "Frontier, on a bounded set of queries."],
    ["**Agentic work** — the go-to-market fleet, onboarding, reading a messy PMS export", "Frontier. Tool use and long loops are not what a 3B fine-tune does."],
    ["**The verifier's judge** on a 10% sample", "Frontier — you want the auditor to be stronger than the author."],
], col_w=[3.5, 2.43], size=9.5, row_h=0.72)
callout(s, 6.9, BODY_Y + 4.05, 5.93, 0.95, None,
        ["The pattern is **cheap model in the loop, strong model at the edges** — and a deterministic verifier over both, so the choice of model stops being a question of trust."],
        fill=PALE, accent=BLUE, body_size=10)

# ---------- 14. Fleet P&L Copilot ----------
s = new_slide("The product is a Fleet P&L Copilot — three surfaces on one governance layer",
              tracker="5 · The products",
              source="Note: WeYield already markets a “Pricing Co-pilot”, so this extends the company's own vocabulary. Residual inputs require the data partnership on slide 16. Sample feed item is illustrative of format only.")
surfaces = [
    ("A", "The Fleet P&L", "The owner's report", ["Per car group, per station, per cohort: revenue, direct cost, **booked depreciation**, **marked-to-market residual**, and the delta.", "No operator in this segment has this. The rental report and the depreciation schedule do not reconcile until the car is sold — two years too late.", "**Build this first.** It changes the buyer before the agent has to be right about anything."], NAVY),
    ("B", "The Decision Feed", "What your agent already does, made defensible", ["Your daily summary, plus: every figure computed, a euro value on every action, and an explicit *what happens if you do nothing*.", "*“Your 2023 diesel Clios reach 24 months in November. De-fleet 40 units now rather than February: est. €68K preserved.”*", "The gap between this and what you have today is the four pieces on slide 12."], BLUE),
    ("C", "The Analyst", "Ask-your-data, grounded, in their language", ["Plain-language questions; every answer traceable to the figures underneath.", "For a craftsman who will not open a dashboard, **the conversation is the interface**.", "Cheapest to build, and the reply channel is where the telemetry comes from."], NAVY),
]
cwp, cgp = 3.98, 0.2
for i, (ltr, hd, sub, body, col) in enumerate(surfaces):
    cx = ML + i * (cwp + cgp)
    rect(s, cx, BODY_Y + 0.05, cwp, 0.8, fill=col)
    text(s, cx + 0.15, BODY_Y + 0.05, 0.5, 0.8, ltr, size=24, color=WHITE, font=SERIF, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(s, cx + 0.7, BODY_Y + 0.1, cwp - 0.85, 0.4, hd, size=13, color=WHITE, font=SERIF, space_after=0)
    text(s, cx + 0.7, BODY_Y + 0.48, cwp - 0.85, 0.35, sub, size=8.5, color=LBLUE, space_after=0)
    rect(s, cx, BODY_Y + 0.85, cwp, 3.0, fill=BG2)
    text(s, cx + 0.18, BODY_Y + 1.0, cwp - 0.36, 2.8, [(b, {'space_after': 7}) for b in body], size=9.5, color=INK, line_spacing=1.1)
rect(s, ML, BODY_Y + 4.0, W - ML - MR, 1.0, fill=NAVY)
text(s, ML + 0.2, BODY_Y + 4.05, 0.5, 0.9, "D", size=24, color=WHITE, font=SERIF, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
text(s, ML + 0.8, BODY_Y + 4.08, 3.2, 0.4, "The governance layer", size=13, color=WHITE, font=SERIF, space_after=0)
text(s, ML + 0.8, BODY_Y + 4.5, 3.6, 0.45, "Guardrails · accept / modify / reject logged · full audit trail", size=8.5, color=LBLUE, line_spacing=1.0, space_after=0)
text(s, ML + 4.6, BODY_Y + 4.08, 7.9, 0.85,
     "Sell **explainable and governed, never autonomous.** For a buyer who cannot audit a model, showing the reasoning is not a compliance feature — it is the only way the recommendation gets acted on. Your whole heritage is teaching these operators to think. **Make explainability the feature, not the apology.**",
     size=9.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1, space_after=0)

# ---------- 15. Rebuild vs never ----------
s = new_slide("Rebuild the layer around the model; never touch the integrations or the numeric core",
              tracker="5 · The products",
              source="Note: gradient-boosted models outperform language models on numeric demand forecasting; the interface, judgement and execution layers wrap around the numeric core. Two-way integration remains the industry's binding constraint.")
lx_, rx_, cw2 = ML, ML + 6.3, 6.03
rect(s, lx_, BODY_Y + 0.05, cw2, 0.6, fill=RULE)
text(s, lx_ + 0.2, BODY_Y + 0.05, cw2 - 0.4, 0.6, "NEVER REWRITE  —  the moat and the risk", size=11, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
rect(s, lx_, BODY_Y + 0.65, cw2, 3.2, fill=BG2)
text(s, lx_ + 0.25, BODY_Y + 0.85, cw2 - 0.5, 3.0, [
    ("**The integration lattice** — Wheels/Invensys, MyRentCar, RateHighway, PMS/CRS write-back. Reliable two-way exchange is the binding constraint in this industry, not modelling. Every integration you have is a mile of track laid.", {'bullet': True}),
    ("**The numeric forecasting core** — gradient-boosted models beat language models at demand forecasting and will continue to.", {'bullet': True}),
    ("**Christian's fine-tune** — it is an asset, not technical debt. Wrap it, do not replace it.", {'bullet': True}),
    ("**The rate-shop collection pipeline** — and extend it to used-car listings rather than building anything new.", {'bullet': True}),
], size=10, line_spacing=1.1, space_after=8)
rect(s, rx_, BODY_Y + 0.05, cw2, 0.6, fill=BLUE)
text(s, rx_ + 0.2, BODY_Y + 0.05, cw2 - 0.4, 0.6, "BUILD — the deterministic layer, and the surfaces", size=11, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
rect(s, rx_, BODY_Y + 0.65, cw2, 3.2, fill=PALE)
text(s, rx_ + 0.25, BODY_Y + 0.85, cw2 - 0.5, 3.0, [
    ("**The facts builder** — every number computed before the model sees it", {'bullet': True}),
    ("**The rules engine** — as data in a table the coach edits, never as code", {'bullet': True}),
    ("**The verifier** — a library every surface imports, with its own tests", {'bullet': True}),
    ("**Telemetry** — recommendation, response, outcome at T+7 and T+28", {'bullet': True}),
    ("**The Fleet P&L screen** — the artefact the owner actually reads", {'bullet': True}),
    ("**Onboarding that reads a messy export** — the only way this buyer ever gets set up", {'bullet': True}),
    ("None of this is model work. All of it is ordinary software, and it is what your fine-tune is currently missing.", {'italic': True, 'color': NAVY, 'space_before': 6}),
], size=10, line_spacing=1.1, space_after=6)
rect(s, ML, BODY_Y + 4.0, W - ML - MR, 1.0, fill=NAVY)
text(s, ML + 0.25, BODY_Y + 4.0, W - ML - MR - 0.5, 1.0,
     "**The discipline that makes it work without a migration project:** from today, every new feature ships in the new layer, and **the old stack receives no new features — maintenance only.** Over eighteen months the new layer absorbs most of the user-facing surface, and the old one shrinks by attrition rather than by decision.",
     size=10.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.12, space_after=0)

# ---------- 16. Data moat ----------
s = new_slide("Four data assets — you hold three of them, and one is rarer than you may realise",
              tracker="5 · The products",
              source="Source: WeYield product footprint per weyield.io and Emmanuel Scuto, 13 September 2026. Indicata (Autorola) and Autovista are candidate partners, not confirmed counterparties. Coverage outside Europe must be checked market by market — the base is worldwide.")
table(s, ML, BODY_Y + 0.05, 8.3, [
    ["Data asset", "Status", "Action"],
    ["**Three years of recorded expert conversation** — every consultant call, with consent", "HELD", "**The rarest thing you own.** It is already in the weights; also keep it as a queryable corpus, or the method stays locked where nobody can read it."],
    ["**Cross-tenant rate shop, pace, utilisation and fleet** — worldwide, not just Europe", "HELD", "Instrument at daily grain per account. Verify 24-month reconstructability. This is the benchmark product."],
    ["**Forward demand signal** — ForwardKeys embedded, IATA under exploration", "HELD", "Deepen. Olivier's own background here is an asset to use."],
    ["**Used-vehicle residual data** — by market, model, specification, mileage, age", "MISSING", "**Partnership, not modelling.** Indicata first. Open it as a data barter: they want rental de-fleet transactions in exactly the secondary markets where you have customers and they have gaps."],
    ["**Recommendation accept / reject telemetry**", "MISSING", "Turn on this month. Cheap now, impossible to backfill, and it is what outcome pricing rests on."],
], col_w=[3.3, 1.35, 3.65], size=9.5, row_h=0.78, status_col=1)
callout(s, 9.05, BODY_Y + 0.05, 3.78, 2.45, "The defensible statement",
        ["**Forward demand + realised pace + used-vehicle residuals + three years of how experts reason.** Nobody holds all four for this segment.",
         "A foundation model cannot acquire the fourth. A funded newcomer cannot buy it. It took you three years of recording to make."], body_size=10)
callout(s, 9.05, BODY_Y + 2.65, 3.78, 2.35, "The risk inside the asset",
        ["A fine-tune is a **write-only** form of knowledge. You cannot read it, diff it, correct one rule in it, or explain a specific answer from it.",
         "Keep the corpus and the rules in a form a human can edit. Otherwise the moat and the black box are the same object."],
        fill=BG2, accent=WARN, body_size=9.5)

# ---------- 17. Three horizons ----------
s = new_slide("Three horizons — and horizon one is shorter than it was, because the model already exists",
              tracker="6 · The plan",
              source="Note: no external capital assumed. Horizon 1 is now about the deterministic layer and pricing, not about building an agent — that work is largely done.")
hz = [
    ("Horizon 1", "Months 0–6", "Make it defensible, and make it pay", "From a demo to a priced product", [
        "**Validate the three kill-risks** — ten customer calls. Gates everything.",
        "**Build the four missing pieces** — facts, rules, verifier, telemetry.",
        "**Reprice the top 20** onto a per-vehicle model. Zero code, ~95% margin.",
        "**AI inside the company** — support, onboarding, config, coaching prep.",
        "**Write the rules down** with the coach — out of the weights, into a table.",
    ], NAVY),
    ("Horizon 2", "Months 6–18", "Change the object and the buyer", "The car, and the owner who buys it", [
        "**Close the residual-data partnership** — Indicata or equivalent. Critical path.",
        "**Ship the Fleet P&L** — the owner's report.",
        "**Move the pricing model** — base + per-vehicle + outcome-linked.",
        "**Enter the operation** — start with the two levers your data already reaches: transfers and de-fleet timing.",
        "**Hire salespeople** — only now, once ACV supports the payback.",
    ], BLUE),
    ("Horizon 3", "Months 18–36", "Compound", "Distribution, not engineering", [
        "**Cross-tenant benchmarking as a product** — the thing no single operator can compute.",
        "**Network Edition** — one franchisor deal reaches 50–200 operators.",
        "**Re-scope the coach** from analyst to supervisor across 5× the accounts — the gross-margin unlock.",
        "**Answer-layer monitoring** — does your customer appear when a traveller asks an assistant?",
    ], NAVY),
]
cwh, cgh = 3.98, 0.2
for i, (hd, mo, obj, metric, steps, col) in enumerate(hz):
    cx = ML + i * (cwh + cgh)
    rect(s, cx, BODY_Y + 0.05, cwh, 1.05, fill=col)
    text(s, cx + 0.18, BODY_Y + 0.1, cwh - 0.36, 0.3, f"{hd.upper()}  ·  {mo.upper()}", size=8, color=LBLUE, bold=True, space_after=0)
    text(s, cx + 0.18, BODY_Y + 0.36, cwh - 0.36, 0.4, obj, size=13, color=WHITE, font=SERIF, space_after=0)
    text(s, cx + 0.18, BODY_Y + 0.74, cwh - 0.36, 0.33, metric, size=8.5, color=LBLUE, space_after=0)
    rect(s, cx, BODY_Y + 1.1, cwh, 3.35, fill=BG2)
    text(s, cx + 0.18, BODY_Y + 1.22, cwh - 0.36, 3.2, [(st, {'bullet': True}) for st in steps], size=9.2, color=INK, line_spacing=1.08, space_after=5)
    if i < 2:
        text(s, cx + cwh - 0.05, BODY_Y + 1.9, cgh + 0.1, 0.5, "›", size=18, color=GREY, align=PP_ALIGN.CENTER, space_after=0)
rect(s, ML, BODY_Y + 4.55, W - ML - MR, 0.45, fill=NAVY)
text(s, ML + 0.2, BODY_Y + 4.55, W - ML - MR - 0.4, 0.45,
     "Sequence: Verify → Price → Cost → Sell → Build. Horizon 1 pays for Horizon 2; Horizon 2 pays for Horizon 3. You never have to ask anyone for money.",
     size=9.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, space_after=0)

# ---------- 18. MVD ----------
s = new_slide("Minimum viable product has become minimum viable distribution",
              tracker="6 · The plan",
              source="Note: the concept Emmanuel asked to keep. Lead-generation channels described by him, 13 September 2026: gated market-trends product, LinkedIn scraping, ERP partner introductions, and an existing contact database.")
text(s, ML, BODY_Y, 12, 0.3, "What changed, and what it means for where effort goes", size=11, color=NAVY, bold=True)
rect(s, ML, BODY_Y + 0.42, 6.1, 1.5, fill=RULE)
text(s, ML + 0.2, BODY_Y + 0.55, 5.7, 0.35, "BEFORE", size=9, color=GREY, bold=True)
text(s, ML + 0.2, BODY_Y + 0.85, 5.7, 0.95, "Building software was hard and expensive. **The product was the moat.** You protected it by shipping features — which is exactly what your team learned to do, and exactly why it never paid.", size=10.5, color=INK, line_spacing=1.15, space_after=0)
rect(s, 6.72, BODY_Y + 0.42, 6.11, 1.5, fill=BLUE)
text(s, 6.92, BODY_Y + 0.55, 5.7, 0.35, "NOW", size=9, color=PALE, bold=True)
text(s, 6.92, BODY_Y + 0.85, 5.7, 0.95, "Building is nearly free, so **ten million people who could not build products now can.** The moat moves to who can reach the customer. **Distribution is the scarce thing.**", size=10.5, color=WHITE, line_spacing=1.15, space_after=0)
text(s, ML, BODY_Y + 2.12, 12, 0.3, "What you already have — and it is more than version 1 credited", size=11, color=NAVY, bold=True)
chans = [
    ("The market-trends product", "Free, gated behind a form. A working lead magnet you already run."),
    ("A contact database", "Built on fifteen years of being the name people know in this category."),
    ("LinkedIn sourcing", "Already scraping for new contacts."),
    ("ERP partner introductions", "You contact their clients on their behalf. **One-to-many, already proven.**"),
]
cxx = ML
for hd, sub in chans:
    rect(s, cxx, BODY_Y + 2.52, 3.03, 1.15, fill=BG2)
    text(s, cxx + 0.16, BODY_Y + 2.64, 2.71, 0.35, hd, size=11, color=NAVY, bold=True, space_after=0)
    text(s, cxx + 0.16, BODY_Y + 2.98, 2.71, 0.6, sub, size=9.5, color=INK, line_spacing=1.1, space_after=0)
    cxx += 3.19
callout(s, ML, BODY_Y + 3.85, 12.33, 1.15, "The one thing to add",
        ["**A free public audit, computed from data you already collect.** Market Radar shops rates for any operator on earth, customer or not. So you can open a conversation with a quantified, provably true statement about their own business — *“you were below all three of your closest competitors on 19 of the last 30 days”* — which nobody else in this market can do. Publish it as a self-serve tool first: the operators who run it on themselves arrive with intent, and with consent."],
        body_size=10)

# ---------- 19. Organisation ----------
s = new_slide("The team does not grow much. What changes is what the nine people are pointed at.",
              tracker="6 · The plan",
              source="Note: current function split inferred from nine employees, one CTO and two in sales; confirm. French employment law makes reduction slow and costly, so the decoupling comes from not hiring.")
table(s, ML, BODY_Y + 0.05, 8.2, [
    ["Function", "Today", "Where it should point"],
    ["**Christian and engineering**", "Building features with unproven return, plus the fine-tune", "The deterministic layer around the model, the integrations, and the data pipeline — the parts that are never rewritten and are the highest-skill work here"],
    ["**The consultants / coaches**", "Delivering expensive analysis by hand, one account at a time", "Owning the rules table, reviewing tier-A briefs, and supervising agents across five times the accounts. **The method moves from their heads into something editable.**"],
    ["**Sales**", "Emmanuel, plus one hire ten months in", "Two to three — but only after ACV supports a twelve-month payback. Repricing first, hiring second."],
    ["**Distribution / performance marketing**", "Digital marketing, self-described as “could be better”", "A named owner with a budget. **This is now the scarce skill, not engineering.**"],
    ["**Emmanuel**", "The only person who can sell, and the reference the market knows", "The same — plus two months inside the tools, because the strategy cannot be delegated to someone who has not felt what the tools do"],
], col_w=[2.1, 2.6, 3.5], size=9.5, row_h=0.78)
callout(s, 8.95, BODY_Y + 0.05, 3.88, 2.4, "The French constraint",
        ["Cutting is slow, expensive, requires documented justification, and signals distress to customers and acquirers alike.",
         "So the decoupling comes from **not hiring**. The nine stay; the next nine are never hired; the work doubles."], body_size=9.5)
rect(s, 8.95, BODY_Y + 2.6, 3.88, 2.4, fill=NAVY)
text(s, 9.15, BODY_Y + 2.72, 3.5, 0.3, "AND THE SUCCESSION QUESTION", size=9, color=LBLUE, bold=True)
text(s, 9.15, BODY_Y + 3.05, 3.5, 1.85,
     "You plan to hand this to your two C-levels in five to six years. **Everything on this page is also the succession plan** — a method locked in one person's head cannot be handed over. A rules table, a verifier and a telemetry history can be.",
     size=10, color=WHITE, line_spacing=1.15, space_after=0)

# ---------- 20. Kill-risks ----------
s = new_slide("Three facts still gate everything — and you have already started testing the first",
              tracker="7 · Risk",
              source="Note: kill-risk 3 uses the same fleet-size-by-account data the repricing exercise needs, so it costs nothing extra. A plan without these tests is a pitch.")
table(s, ML, BODY_Y + 0.05, W - ML - MR, [
    ["Kill-risk", "Why it kills the thesis", "Status after 13 Sep", "If it fails"],
    ["**1 · Buyback exposure**", "Customers still on OEM buyback do not own residual risk, so the Fleet P&L has no buyer.", "**In progress.** You have been discussing the car question with customers for two days and will continue. Ten structured calls finishes it.", "Thesis narrows to the owned-at-risk segment; size it first. The move and substitute levers survive regardless."],
    ["**2 · Fleet financials in the PMS**", "If acquisition cost, in-service date, mileage and disposal are absent from the integrated systems, the product becomes data entry — which this buyer will never do.", "**Open, and now more worrying.** You describe the ERPs as slow and unsophisticated, serving unsophisticated buyers. Assume the fields are thin.", "First release becomes a fleet-data ingestion product. Six to nine months longer."],
    ["**3 · Fleet-size distribution**", "Below roughly 200 cars, de-fleet decisions are too lumpy to optimise and value per account will not support the ACV step-up.", "**Open.** With ten-car and fifty-car operators in the base, the distribution matters more than version 1 assumed.", "The fleet product is a top-quartile offer, not a platform offer. Viable, but a different sales model."],
], col_w=[2.1, 3.6, 3.5, 3.13], size=9.5, row_h=1.2)
rect(s, ML, BODY_Y + 4.35, W - ML - MR, 0.65, fill=NAVY)
text(s, ML + 0.25, BODY_Y + 4.35, W - ML - MR - 0.5, 0.65,
     "**A fourth risk, new in version 2:** the method now lives inside a fine-tune. If Christian leaves, or the model needs retraining, or a customer disputes an answer — there is no artefact to point at. Getting the rules out of the weights and into a table is a **succession** issue as much as a product one.",
     size=10, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1, space_after=0)

# ---------- 21. Six decisions ----------
s = new_slide("Six decisions for this week",
              tracker="7 · Risk",
              source="Note: decisions 1, 2 and 5 cost nothing. Decision 3 is a policy change with immediate effect. Decision 6 is a commercial conversation whose lead time exceeds any integration.")
decs = [
    ("Get on the tools yourself, properly", "The €200-a-year plan will not show you anything. Take the €100-a-month plan and the command line for two months. The strategy cannot be delegated to someone who has not felt what the tools do.", "Emmanuel", "This week"),
    ("Finish the ten customer calls on the car question", "Buyback mix, fleet-data fields, fleet size. You have started. Structure it and finish it — it gates everything else.", "Emmanuel", "Week 1"),
    ("Turn on recommendation telemetry", "What the agent recommended, what the customer did, what happened. Cheap today, impossible to reconstruct later.", "Christian", "Week 1"),
    ("Get the rules out of the weights", "Sit with a coach and write down ten rules as a table. Not as marketing — as specification the engine can execute and a human can edit.", "Coach + Christian", "Weeks 1–3"),
    ("Pull the fleet size behind every top-20 account", "Then run per-vehicle pricing against them. If those numbers cannot be produced, that is itself the finding of the week.", "Sales", "Week 1"),
    ("Open the Indicata conversation as a data barter", "Critical path for Horizon 2. Commercial negotiations take longer than integrations, so it starts now, not when the module is designed.", "Emmanuel", "Week 2"),
]
yy = BODY_Y + 0.05
for i, (hd, body, owner, when) in enumerate(decs):
    rect(s, ML, yy, 0.55, 0.72, fill=(BLUE if i < 2 else NAVY))
    text(s, ML, yy, 0.55, 0.72, str(i + 1), size=18, color=WHITE, font=SERIF, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    rect(s, ML + 0.55, yy, W - ML - MR - 0.55, 0.72, fill=(BG2 if i % 2 == 0 else WHITE), line=None)
    text(s, ML + 0.75, yy + 0.06, 3.3, 0.6, hd, size=11, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0, space_after=0)
    text(s, ML + 4.15, yy + 0.06, 5.6, 0.6, body, size=9.5, color=INK, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.08, space_after=0)
    text(s, ML + 9.85, yy + 0.06, 1.25, 0.6, owner, size=9, color=GREY, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(s, ML + 11.15, yy + 0.06, 1.08, 0.6, when, size=9, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT, space_after=0)
    hline(s, ML + 0.55, yy + 0.72, W - ML - MR - 0.55, color=RULE)
    yy += 0.78
text(s, ML + 0.75, BODY_Y - 0.02, 3, 0.25, "DECISION", size=7.5, color=GREY, bold=True, space_after=0)
text(s, ML + 9.85, BODY_Y - 0.02, 1.25, 0.25, "OWNER", size=7.5, color=GREY, bold=True, space_after=0)
text(s, ML + 11.15, BODY_Y - 0.02, 1.08, 0.25, "WHEN", size=7.5, color=GREY, bold=True, align=PP_ALIGN.RIGHT, space_after=0)
text(s, ML, BODY_Y + 4.78, W - ML - MR, 0.3,
     "The real risk is not choosing the wrong AI strategy. It is spending 2027 deciding.",
     size=12, color=NAVY, font=SERIF, align=PP_ALIGN.CENTER, space_after=0)

# ---------- 22. Appendix ----------
s = new_slide("Appendix — what is given, what is derived, what is assumed, and what still conflicts",
              tracker="Appendix",
              source="Prepared by Ram Badrinathan, 14 September 2026. Version 2, rewritten after the conversation with Emmanuel Scuto of 13 September 2026.")
table(s, ML, BODY_Y + 0.05, W - ML - MR, [
    ["Category", "Figures", "Treatment"],
    ["**Given — Emmanuel, 13 Sep**", "Founded 2012 · 100+ customers of a workable ~1,000 · worldwide, not Europe-centric · no profit in ten years · 9 people · Christian CTO · one sales hire, 10 months · exit in 5–6 years to the two C-levels · 60–70% of operator cost is the car · 3 years of recorded calls · 3B fine-tune at 95–97%, self-hosted", "As stated in conversation. Not verified against company records."],
    ["**Given — Olivier, 10 Sep**", "€1.5M revenue · ~4% operator net margin · ~€2M standing offer · 10–15% growth", "As reported. **Two items conflict with Emmanuel's account** — see the last row."],
    ["**Derived**", "~10% market penetration · implied ACV · TAM at current pricing · Rule of 40", "Arithmetic on the given figures only."],
    ["**Assumed — not verified**", "€700 revenue per unit per month · €22K acquisition · €15K disposal · ancillary share and margin · loaded salesperson cost · cost-to-serve lines · all three-year projections", "**Invented to show a mechanism and its order of magnitude.** Every one is listed with its location in OPEN-QUESTIONS.md. Correct any and the exhibit should be redrawn."],
    ["**Unresolved conflicts**", "**Exit horizon:** Olivier says two to three years and a sale; Emmanuel says five to six and a handover to his C-levels. **Deal size:** “under €40,000” against an implied average nearer €12,500.", "Both change what the plan optimises for. Worth settling before this deck goes to anyone else."],
], col_w=[1.9, 6.0, 4.43], size=9.5, row_h=0.95)

prs.save(OUT)
print("WROTE", OUT, "slides:", len(prs.slides))
