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
rect(s, ML, 1.55, 0.9, 0.06, fill=BLUE)
text(s, ML, 1.8, 10.5, 1.9, ["Building the", "AI-native WeYield"], size=44, color=WHITE, font=SERIF, line_spacing=1.0, space_after=0)
text(s, ML, 3.75, 9.5, 0.9, "From rate optimisation for revenue managers to fleet P&L optimisation for owners",
     size=16, color=LBLUE, line_spacing=1.15)
text(s, ML, 5.05, 8, 0.9, [("Strategic recommendation", {'bold': True, 'size': 12, 'color': WHITE, 'space_after': 3}),
                            ("Prepared for Emmanuel Scuto, Chief Executive Officer", {'size': 11, 'color': LBLUE, 'space_after': 3}),
                            ("Ram Badrinathan  ·  September 2026", {'size': 11, 'color': LBLUE})])
hline(s, ML, 6.7, W - ML - MR, color=RGBColor(0x2A, 0x3F, 0x52), weight=0.5)
text(s, ML, 6.8, 8, 0.3, "PRELIMINARY — FOR DISCUSSION  ·  CONFIDENTIAL", size=8, color=LBLUE)
text(s, 8.8, 6.8, 4.0, 0.3, "Figures as reported 10 September 2026; not verified against company accounts", size=8, color=LBLUE, align=PP_ALIGN.RIGHT)

# ---------- 2. Executive summary ----------
s = new_slide("Executive summary — WeYield should stop selling rates to revenue managers and start selling fleet P&L to owners; AI is what makes that affordable",
              tracker="Executive summary",
              source="Source: Olivier Jager strategic review and briefing call, 10 Sep 2026; The AI Turn for WeYield (Sep 2026); analysis. Year-3 figures illustrative — see appendix for treatment of every number.")
pts = [
    ("**A sound business with broken operating leverage.** €1.5M revenue, ~120 customers, 10–15% growth, EBITDA flat to contracting. The standing ~€2M offer (1.3× revenue) is the correct price for that profile — not a lowball.", {}),
    ("**The current product is structurally capped.** Car rental operators pull five levers — price, move, substitute, buy, sell. WeYield optimises price and sizes the fleet for demand; **nobody in this market optimises the fleet for value.** At €12.5K implied ACV, the entire addressable market is ~€7.5M.", {}),
    ("**The profit sits in a bracket WeYield does not touch.** Operator net margin is ~4%; the year's result is decided at remarketing. A 1% gain in residual realisation is worth 20–45% of a 1,000-car operator's annual profit.", {}),
    ("**Five conditions converged since 2021.** OEM buyback contraction moved residual risk to the long tail; EV/diesel volatility broke intuition; used-car data became an API; language models collapsed cost-to-serve; RateHighway is commoditising the pricing engine.", {}),
    ("**Recommendation — three changes in strict sequence.** Change the object (rate → fleet plan), the buyer (revenue manager → owner) and the cost-to-serve (consultant-led → AI-native). Rebuild the interface and agent layer; never touch the integrations or the numeric core.", {}),
    ("**Self-funding across three horizons; illustratively €4.8M at ~31% EBITDA in Year 3**, headcount 9 → 16 by not hiring rather than cutting. Three kill-risks — buyback exposure, PMS fleet-data coverage, fleet-size distribution — are testable in two weeks and gate every line of code.", {}),
]
yy = BODY_Y + 0.05
for i, (t, o) in enumerate(pts):
    rect(s, ML, yy + 0.04, 0.34, 0.34, fill=NAVY)
    text(s, ML, yy + 0.04, 0.34, 0.34, str(i + 1), size=11, color=WHITE, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(s, ML + 0.5, yy, W - ML - MR - 0.5, 0.8, t, size=11, color=INK, line_spacing=1.12, space_after=0)
    yy += 0.84

# ---------- 3. Starting position ----------
s = new_slide("WeYield is a sound, growing €1.5M business whose EBITDA has stopped responding to revenue",
              tracker="1 · Where WeYield stands",
              source="Source: Olivier Jager, strategic review of 10 Sep 2026 and briefing call. All figures as reported; none verified against company accounts. ACV is derived (€1.5M ÷ 120).")
tiles = [
    ("€1.5M", "Annual revenue", "Growing 10–15% p.a."),
    ("~120", "Paying customers", "600–1,000 addressable"),
    ("€12.5K", "Implied average ACV", "Reported top deals <€40K"),
    ("9", "Employees", "2 in sales; ~5 in product"),
    ("~0%", "EBITDA margin", "Flat; contracting in periods"),
    ("12–20%", "Market penetration", "Described as “embryonic”"),
    ("50+", "Countries served", "EU core; islands, N. Africa, NZ"),
    ("~€2M", "Standing acquisition offer", "1.3× revenue; exit intent 2–3 yrs"),
]
tx, ty, tw, th, tg = ML, BODY_Y + 0.05, 1.98, 1.42, 0.16
for i, (v, l, sub) in enumerate(tiles):
    r_, c_ = divmod(i, 4)
    kpi(s, tx + c_ * (tw + tg), ty + r_ * (th + tg), tw, th, v, l, sub, accent=(BLUE if i in (4, 7) else NAVY))
callout(s, 9.2, BODY_Y + 0.05, 3.63, 3.0, "The point of vigilance",
        ["Sales have grown every year since founding. EBITDA has not moved — and has contracted in some periods.",
         "**Working hypothesis (Olivier):** the company's strength — a strong product team and permanent product investment — is also its weakness. New features show no demonstrable return.",
         "**Implication:** the financial value of a healthy, stable business is in question."], body_size=9.5)
callout(s, 9.2, BODY_Y + 3.22, 3.63, 1.15, "Three numbers still to reconcile",
        ["“Average deal <€40K” vs €12.5K implied  ·  600 vs 600–1,000 addressable  ·  “120 customers” vs “100+ users”. See appendix."],
        fill=BG2, accent=GREY, body_size=9)

# ---------- 4. Rule of 40 ----------
s = new_slide("The ~€2M offer is not a lowball — it is the correct price for a business growing 15% at zero margin",
              tracker="1 · Where WeYield stands", sticker="Indicative",
              source="Note: Rule of 40 = revenue growth % + EBITDA margin %. Multiple ranges are indicative for vertical B2B SaaS and are not a valuation opinion. Year-3 score uses the illustrative plan in section 5.")
text(s, ML, BODY_Y, 6.6, 0.3, "Rule of 40 score", size=11, color=NAVY, bold=True)
text(s, ML, BODY_Y + 0.28, 6.6, 0.3, "Growth % + EBITDA margin %", size=9, color=GREY)
hbars(s, ML, BODY_Y + 0.85, 6.6, [
    ("WeYield today\n15% growth + ~0% EBITDA", 15, MID, "~15"),
    ("Year 3, illustrative plan\n50% growth + 31% EBITDA", 81, BLUE, "~81"),
], max_val=100, label_w=2.7, bar_h=0.55, gap=0.55, threshold=40, threshold_label="Rule of 40", label_size=9.5)
text(s, 7.6, BODY_Y, 5.2, 0.3, "What the market pays for each profile", size=11, color=NAVY, bold=True)
table(s, 7.6, BODY_Y + 0.42, 5.23, [
    ["Rule of 40 score", "Indicative revenue multiple", "Where WeYield sits"],
    ["Below 20", "1–2×", "**Today: 1.3× (~€2M)**"],
    ["20–40", "2–3×", "—"],
    ["Above 40", "4–6×", "Year 3 plan (illustrative)"],
], col_w=[1.55, 1.85, 1.83], size=9.5, row_h=0.4)
callout(s, 7.6, BODY_Y + 2.45, 5.23, 1.75, "The point to make to the board",
        ["The offer is not a valuation of WeYield. It is a **measurement of the current operating model.**",
         "Every recovered EBITDA point moves the number. Nothing in the AI narrative moves it on its own."], body_size=10)
callout(s, ML, BODY_Y + 3.55, 6.6, 1.0, None,
        ["Two roads — independent AI-native category leader, or attractive acquisition for a consolidator — **run through the identical eighteen months of work.** There is no strategic fork requiring a decision today; only work to start."],
        fill=BG2, accent=NAVY, body_size=10)

# ---------- 5. TAM ceiling ----------
s = new_slide("Even at 100% share, the current product tops out near €7.5M — this is a ceiling, not a sales-coverage gap",
              tracker="1 · Where WeYield stands",
              source="Source: derived — addressable market of 600–1,000 operators (Olivier Jager, 10 Sep 2026) × €12.5K implied ACV. Realistic ceiling assumes a 35–40% share of the 600–1,000, which no vendor in a fragmented vertical exceeds.")
text(s, ML, BODY_Y, 7.6, 0.3, "Revenue potential of the current product at current pricing, €M", size=11, color=NAVY, bold=True)
vcols(s, ML, BODY_Y + 0.4, 7.6, 4.5, [
    ("Today\n~120 accounts", 1.5, NAVY),
    ("Realistic ceiling\n35–40% share", 4.5, BLUE),
    ("600 accounts\n100% share", 7.5, MID),
    ("1,000 accounts\n100% share", 12.5, RULE),
], max_val=13.5, fmt=lambda v: f"€{v:g}M", label_size=9.5, value_size=13)
callout(s, 8.6, BODY_Y + 0.1, 4.23, 1.95, "You cannot sell your way out of a TAM ceiling",
        ["Perfect sales execution on the current product makes WeYield a €4–5M company. That is the arithmetic behind Olivier's *remontée dans la chaîne de valeur* — it is mandatory, not aspirational.",
         "There are only two exits: **price up**, or **move up the stack**. The recommendation is both."], body_size=10)
callout(s, 8.6, BODY_Y + 2.2, 4.23, 2.05, "Why franchisees make it worse",
        ["A material share of the base are Hertz, Avis, Europcar and Sixt franchisees. They pay a royalty, receive the brand and the reservation feed — and **do not hold full rate autonomy.**",
         "WeYield is therefore selling partial control of the weakest lever, while the four levers the customer fully controls go untouched."], fill=BG2, accent=GREY, body_size=9.5)

# ---------- 6. Rep payback ----------
s = new_slide("At €12.5K ACV a salesperson barely pays back in year one — hiring reps first would not repair EBITDA",
              tracker="1 · Where WeYield stands", sticker="Illustrative",
              source="Assumptions: two reps produce the reported 10–15% growth (~€170K new ARR p.a.) → ~7 new logos per rep per year; fully loaded French sales cost €90K. Payback = loaded cost ÷ first-year ARR landed. Logo velocity held constant across ACV scenarios.")
text(s, ML, BODY_Y, 7.4, 0.3, "Months for a new rep to pay back a €90K loaded cost, by ACV", size=11, color=NAVY, bold=True)
text(s, ML, BODY_Y + 0.28, 7.4, 0.3, "~7 new logos per rep per year", size=9, color=GREY)
hbars(s, ML, BODY_Y + 0.85, 7.4, [
    ("€12.5K ACV — today", 13, MID, "~13 months"),
    ("€16K ACV — after top-20 repricing", 10, LBLUE, "~10 months"),
    ("€22K ACV — with the fleet module", 7, BLUE, "~7 months"),
], max_val=15, label_w=2.9, bar_h=0.5, gap=0.42, label_size=10)
callout(s, 8.4, BODY_Y + 0.1, 4.43, 1.8, "Olivier's prescription is right and mistimed",
        ["“Move money from product to sales” is directionally correct. But at €12.5K a rep returns ~€85K of new ARR against €80–100K of cost. **The unit does not pay for the rep fast enough.**",
         "That is why Emmanuel has not hired — and why he should not yet."], body_size=10)
rect(s, 8.4, BODY_Y + 2.1, 4.43, 1.8, fill=NAVY)
text(s, 8.65, BODY_Y + 2.25, 4.0, 0.4, "The sequence this forces", size=10, color=LBLUE, bold=True)
text(s, 8.65, BODY_Y + 2.62, 4.0, 1.25, [("Price  →  Cost  →  Sell  →  Build", {'size': 17, 'color': WHITE, 'font': SERIF, 'space_after': 8}),
                                          ("Reprice the top 20 accounts first. Fix cost-to-serve. *Then* hire salespeople three and four. *Then* build.", {'size': 9.5, 'color': LBLUE})], line_spacing=1.1)

# ---------- 7. Five levers ----------
s = new_slide("Car rental is not hotel revenue management: WeYield sizes the fleet for demand — no one in this market optimises it for value",
              tracker="2 · Why the product is capped",
              source="Status column inferred from weyield.io product and role pages (Sep 2026): Performance Hub and Revenue Horizon analyse fleet; the Revenue Manager page claims “fleet and price optimization” — verify on the call. ACRISS/SIPP codes (e.g. ECMR) define the substitution ladder. Franchisee rate autonomy varies by franchisor.")
callout(s, ML, BODY_Y + 0.05, 3.5, 4.95, "The structural difference",
        ["**In hotels, inventory is fixed.** Room 301 exists whether or not it is sold, cannot be moved to another city, and cannot be sold off at season end. Rate is the only lever — so an RMS that optimises rate is a *complete* product.",
         "**In car rental, inventory is mobile, substitutable and disposable.** The operator has five levers. WeYield prices, and plans the fleet against demand. Nobody tells the owner what the fleet is *worth*, or when to sell it.",
         "That gap — not sales coverage, and not AI — is the mechanical reason ACV sits at €12.5K."], body_size=10)
table(s, 4.25, BODY_Y + 0.05, 8.58, [
    ["Lever", "The decision", "Who makes it today", "WeYield today"],
    ["**Price**", "Rate by car group, channel, booking window, length of rental", "Revenue manager — WeYield's user. Franchisees control it only partly", "Covered"],
    ["**Move**", "Transfer units between stations to meet peak demand (Jaipur → Udaipur)", "Operations, by instinct", "Analytics only — utilisation reported, no redistribution recommended"],
    ["**Substitute**", "Walk the customer up the ACRISS ladder (ECMR → CDMR)", "Counter staff, ad hoc", "Not covered"],
    ["**Buy**", "How many of each group, when, at what acquisition cost — and what they will be worth", "Owner, annually, by gut", "Demand-side only — no cost or residual view"],
    ["**Sell**", "When to de-fleet each cohort — the decision that sets the year's profit", "Owner, by gut or by lease expiry", "Demand-side only — no residual view"],
], col_w=[1.1, 3.05, 2.55, 1.88], size=9.5, row_h=0.62, status_col=3)

# ---------- 8. Profit equation ----------
s = new_slide("The operator's profit is made on the residual, not the rental — a bracket WeYield does not touch",
              tracker="2 · Why the product is capped", sticker="Illustrative",
              source="Assumptions: 1,000-vehicle operator; €700 revenue per unit per month (€8.4M p.a.); 4% net margin as cited by Olivier Jager; €15K average disposal value; 24-month holding period, so ~500 disposals p.a. Hertz Tesla write-down per public filings, 2023–24.")
# equation row
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
eqbox(6.2, 3.9, "Residual realised − Depreciation booked", "Where the volatility and often the whole margin live · unserved", BLUE, WHITE, PALE)
op(10.1, "−")
eqbox(10.5, 2.33, "Holding cost", "financing, insurance, storage", RULE, INK, GREY)
# sizing exhibit
text(s, ML, BODY_Y + 1.4, 7.2, 0.3, "Sizing the second bracket for a 1,000-vehicle operator, €K per year", size=11, color=NAVY, bold=True)
hbars(s, ML, BODY_Y + 1.9, 7.2, [
    ("Annual net profit at 4% margin", 336, MID, "€336K"),
    ("Value of +1% residual realisation — low case", 75, LBLUE, "€75K  (22% of profit)"),
    ("Value of +1% residual realisation — high case", 150, BLUE, "€150K  (45% of profit)"),
], max_val=400, label_w=3.1, bar_h=0.42, gap=0.34, value_w=1.9, label_size=9.5)
callout(s, 8.1, BODY_Y + 1.45, 4.73, 1.65, "Booked vs realised",
        ["Depreciation is *booked* as an estimate at acquisition and *realised* years later at remarketing. Book €300/month, lose €380, and a year of operating profit is gone."], body_size=9.5)
callout(s, 8.1, BODY_Y + 3.2, 4.73, 1.5, "This happens to professionals too",
        ["Hertz wrote down roughly **$2.9bn** on Tesla residuals in 2023–24 — this bracket, at scale, with an in-house fleet team. The long tail has no team and, since 2021, increasingly carries the risk itself."],
        fill=BG2, accent=GREY, body_size=9.5)

# ---------- 9. Why now ----------
s = new_slide("Five conditions have converged since 2021 that make this urgent rather than merely attractive",
              tracker="2 · Why the product is capped",
              source="Source: industry reporting on OEM repurchase programmes post-2021; Hertz/Tesla residual write-downs; Indicata, Autovista, BCA, Manheim data products; RateHighway Enhanced Intelligence and Rexalto AMPE partnership (The AI Turn for WeYield, Sep 2026).")
conds = [
    ("The risk moved to the customer", "OEM buyback and repurchase programmes contracted sharply after the 2021 semiconductor shortage. The long tail now carries residual exposure it never held — and in many cases does not yet see on its management reporting."),
    ("The risk got harder", "EV residual collapse and European diesel demand shifts destroyed the intuitions that used to substitute for a model. Olivier's own point — Middle Eastern supply chains dictating resale values — is exactly this."),
    ("The missing input became purchasable", "Used-vehicle market intelligence is now an API: Indicata (live pan-European stock, price, days-to-sell), Autovista (residual forecasts), BCA and Manheim (auction). Five years ago this was a licensing project."),
    ("The delivery cost collapsed", "Schema mapping, car-group normalisation, seasonality inference, onboarding, configuration and tier-one support — the costs that made a €12K account unservable — are precisely what language models do well. This is a cost argument, not a capability argument."),
    ("Standing still stopped being safe", "RateHighway — a partner — is building an expandable pricing-engine framework and has plugged in a third-party engine. A pricing engine inside someone else's store is a commodity. The only exit is upward."),
]
cw_, cg_ = 2.37, 0.12
for i, (hd, body) in enumerate(conds):
    cx = ML + i * (cw_ + cg_)
    rect(s, cx, BODY_Y + 0.05, cw_, 0.62, fill=NAVY if i != 4 else BLUE)
    text(s, cx + 0.12, BODY_Y + 0.05, 0.5, 0.62, str(i + 1), size=22, color=WHITE, font=SERIF, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(s, cx + 0.55, BODY_Y + 0.05, cw_ - 0.65, 0.62, hd, size=10, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05, space_after=0)
    rect(s, cx, BODY_Y + 0.67, cw_, 2.95, fill=BG2)
    text(s, cx + 0.15, BODY_Y + 0.82, cw_ - 0.3, 2.75, body, size=9.5, color=INK, line_spacing=1.12)
text(s, ML, BODY_Y + 3.85, W - ML - MR, 0.5, "Any three of these would make the fleet thesis interesting. All five make it urgent.",
     size=13, color=NAVY, font=SERIF, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 10. Stack / RateHighway ----------
s = new_slide("Staying a pricing engine means becoming a plugin in someone else's platform — the only exit is up the stack",
              tracker="2 · Why the product is capped",
              source="Source: The AI Turn for WeYield (Sep 2026) — RateHighway expandable pricing framework; Expedia in Google AI Mode (Aug 2026); Otto The Agent car rental (Jul 2026); Sabre/PayPal/MindTrip pipeline (Feb 2026); M. Meyer, Auto Rental News, Mar and Sep 2026.")
text(s, ML, BODY_Y, 12, 0.3, "The car rental distribution chain, and where the pressure now sits", size=11, color=NAVY, bold=True)
layers = [
    ("Owner's fleet P&L", "buy · sell · move · size", BLUE, WHITE, "WEYIELD TARGET"),
    ("Revenue strategy", "coaching · pace · rate decisions", NAVY, WHITE, "WEYIELD TODAY"),
    ("Rate engine platform", "RateHighway — hosting any engine", RULE, INK, "COMMODITISING"),
    ("Reservation system", "PMS / CRS write-back", BG2, INK, None),
    ("Channels", "OTA · broker · direct", BG2, INK, None),
    ("AI interpretation layer", "Google AI Mode · Otto · MindTrip", RULE, INK, "NEW · UNMONITORED"),
    ("Traveller", "asks, compares, books", BG2, INK, None),
]
lw, lg = 1.68, 0.1
ly = BODY_Y + 0.75
for i, (hd, sub, fill, col, tag) in enumerate(layers):
    lx = ML + i * (lw + lg)
    rect(s, lx, ly, lw, 1.25, fill=fill)
    text(s, lx + 0.1, ly + 0.12, lw - 0.2, 0.5, hd, size=10.5, color=col, bold=True, line_spacing=1.0, space_after=0)
    text(s, lx + 0.1, ly + 0.66, lw - 0.2, 0.55, sub, size=8.5, color=(LBLUE if fill in (BLUE, NAVY) else GREY), line_spacing=1.0, space_after=0)
    if tag:
        text(s, lx, ly - 0.32, lw, 0.28, tag, size=7.5, color=(BLUE if i == 0 else (NAVY if i == 1 else RED)), bold=True, align=PP_ALIGN.CENTER, space_after=0)
    if i < len(layers) - 1:
        text(s, lx + lw - 0.02, ly + 0.4, lg + 0.06, 0.45, "›", size=16, color=GREY, align=PP_ALIGN.CENTER, space_after=0)
callout(s, ML, BODY_Y + 2.4, 4.05, 2.0, "Pressure from below: the engine is being commoditised",
        ["RateHighway's framework hosts third-party pricing engines. A platform that hosts engines does not need to be the best engine — it needs the most engines. **If WeYield stays a rate engine, it becomes a plugin.**"], body_size=9.5)
callout(s, 4.75, BODY_Y + 2.4, 4.05, 2.0, "Pressure from the right: the rate sent is no longer the rate seen",
        ["AI assistants now rewrite the traveller's question, choose which sources to inspect, rank, and transact. An operator can be priced correctly and still be invisible, misquoted, or compared against the wrong car class. **Nobody monitors this yet.**"], fill=BG2, accent=GREY, body_size=9.5)
callout(s, 9.0, BODY_Y + 2.4, 3.83, 2.0, "The exit: up, to the owner's P&L",
        ["The one layer no platform is building for the long tail is the owner's decision layer — fleet sizing, buy/sell timing, redistribution. It sits above the rate engine, it changes the buyer, and it is where the margin is."], fill=NAVY, accent=BLUE, body_size=9.5)
# recolor navy callout text to white
for shp in list(s.shapes)[-2:]:
    if shp.has_text_frame:
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                r.font.color.rgb = WHITE if r.font.bold else LBLUE

# ---------- 11. Recommendation ----------
s = new_slide("Recommendation — change the object, the buyer and the cost-to-serve, in that order",
              tracker="3 · The recommendation",
              source="Note: the three changes are sequenced, not parallel. Change 3 makes 1 and 2 affordable; change 1 makes 2 credible. Run in parallel, the result is an expensive fleet module sold to a revenue manager with no budget for it.")
cols3 = [
    ("1", "Change the object", "The rate", "The fleet plan — five levers, not one", "Price, move, substitute, buy, sell. The unit of analysis becomes the fleet cohort across stations and weeks, not the rate on a car group.", NAVY),
    ("2", "Change the buyer", "Revenue manager — tool budget, €12.5K", "Owner / general manager — P&L, €50K+", "WeYield already courts this buyer — its site lists “CEO & Managing Director: strategy and financial performance” — but has nothing a CEO reads. The Fleet P&L is that artefact. Owners have a P&L; clerks have a tool budget: the gap between a €12K and a €60K contract.", BLUE),
    ("3", "Change the cost-to-serve", "Consultant-led implementation and human coaching", "AI-native onboarding, configuration, advisory", "The only way to reach the 480–880 operators WeYield does not have. This is a cost argument; it makes 1 and 2 affordable.", NAVY),
]
cw3, cg3 = 3.98, 0.2
for i, (n, hd, frm, to, why, col) in enumerate(cols3):
    cx = ML + i * (cw3 + cg3)
    rect(s, cx, BODY_Y + 0.05, cw3, 0.75, fill=col)
    text(s, cx + 0.15, BODY_Y + 0.05, 0.6, 0.75, n, size=26, color=WHITE, font=SERIF, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(s, cx + 0.75, BODY_Y + 0.05, cw3 - 0.9, 0.75, hd, size=14, color=WHITE, font=SERIF, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    rect(s, cx, BODY_Y + 0.8, cw3, 3.55, fill=BG2)
    text(s, cx + 0.2, BODY_Y + 0.95, cw3 - 0.4, 0.3, "FROM", size=8, color=GREY, bold=True, space_after=0)
    text(s, cx + 0.2, BODY_Y + 1.2, cw3 - 0.4, 0.7, frm, size=11, color=INK, line_spacing=1.05, space_after=0)
    text(s, cx + 0.2, BODY_Y + 1.95, cw3 - 0.4, 0.3, "TO", size=8, color=col, bold=True, space_after=0)
    text(s, cx + 0.2, BODY_Y + 2.2, cw3 - 0.4, 0.7, to, size=12, color=NAVY, bold=True, line_spacing=1.05, space_after=0)
    hline(s, cx + 0.2, BODY_Y + 2.98, cw3 - 0.4, color=RULE)
    text(s, cx + 0.2, BODY_Y + 3.08, cw3 - 0.4, 1.2, why, size=9.5, color=INK, line_spacing=1.1, space_after=0)
rect(s, ML, BODY_Y + 4.5, W - ML - MR, 0.5, fill=NAVY)
text(s, ML + 0.2, BODY_Y + 4.5, W - ML - MR - 0.4, 0.5, "AI is not the product. AI is what makes it economically possible to serve 600–1,000 fragmented operators with something that previously required a consulting engagement per client.",
     size=10.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, space_after=0)

# ---------- 12. Product ----------
s = new_slide("The product is a Fleet P&L Copilot — three surfaces on one governance layer",
              tracker="3 · The recommendation",
              source="Note: WeYield already markets a “Pricing Co-pilot” inside Pricing Insights — the Fleet P&L Copilot extends the company's own vocabulary. Sample Decision Feed item is illustrative of format; residual inputs require the partnership on slide 14. Black-box distrust as the adoption blocker: Auto Rental News, Mar 2026.")
surfaces = [
    ("A", "The Fleet P&L", "The owner's report", ["Per car group, per station, per cohort: revenue, direct cost, **booked depreciation**, **marked-to-market residual**, and the delta.", "No long-tail operator has this today — the rental report and the depreciation schedule do not reconcile until the car is sold, two years too late.", "**Build this first.** It changes the buyer before the agent has to be right about anything."], NAVY),
    ("B", "The Decision Feed", "One ranked daily list across five levers", ["Each item carries a euro value, a confidence, and an explicit *what happens if you do nothing*.", "*“Your 2023 diesel Clios reach 24 months in November. French B-segment diesel residuals are off 3.1% over 90 days and days-to-sell is lengthening. De-fleet 40 units now rather than February: est. €68K preserved.”*", "That sentence is not producible by any product in this market today."], BLUE),
    ("C", "The Analyst", "Ask-your-data, grounded, multilingual", ["Plain-language questions over the Performance Hub; every answer traceable to the underlying figures.", "Cheapest to build, strongest demo, cannot lose a customer money. Multilingual is nearly free — material across 50 countries.", "**The wedge, not the strategy.**"], NAVY),
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
text(s, ML + 0.8, BODY_Y + 4.08, 3.0, 0.4, "The governance layer", size=13, color=WHITE, font=SERIF, space_after=0)
text(s, ML + 0.8, BODY_Y + 4.5, 3.4, 0.45, "Guardrails set by the operator · accept / modify / reject logged · full audit trail", size=8.5, color=LBLUE, line_spacing=1.0, space_after=0)
text(s, ML + 4.6, BODY_Y + 4.08, 7.9, 0.85, "Sell **explainable and governed, never autonomous.** The named adoption blocker in this industry is black-box distrust. WeYield's whole heritage — the Academy, the coaches, teaching operators to think — makes *“the agent shows its reasoning and you keep the wheel”* the natural position. Make explainability the feature, not the apology.",
     size=9.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1, space_after=0)

# ---------- 13. Rebuild vs never ----------
s = new_slide("Rebuild the interface and agent layer AI-natively; never touch the integrations or the numeric core",
              tracker="3 · The recommendation",
              source="Note: gradient-boosted and related numeric models outperform language models at demand forecasting on structured time series; the interface, judgement, explanation and execution layers wrap around the numeric core. Two-way integration is the industry's binding constraint (M. Meyer, Auto Rental News, Mar 2026).")
lx_, rx_, cw2 = ML, ML + 6.3, 6.03
rect(s, lx_, BODY_Y + 0.05, cw2, 0.6, fill=RULE)
text(s, lx_ + 0.2, BODY_Y + 0.05, cw2 - 0.4, 0.6, "NEVER REWRITE  —  the moat and the risk", size=11, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
rect(s, lx_, BODY_Y + 0.65, cw2, 3.2, fill=BG2)
text(s, lx_ + 0.25, BODY_Y + 0.85, cw2 - 0.5, 3.0, [
    ("**The integration lattice** — Wheels/Invensys, MyRentCar, RateHighway, PMS/CRS write-back. Reliable two-way data exchange is the industry's binding constraint, not modelling. Every integration already built is a mile of track laid.", {'bullet': True}),
    ("**The numeric forecasting core** — gradient-boosted models beat language models at numeric demand forecasting and will continue to. Confusing the interface layer with the numeric layer burns a year.", {'bullet': True}),
    ("**The rate-shop collection pipeline.**", {'bullet': True}),
    ("Rewriting these buys nothing and can lose customers.", {'italic': True, 'color': GREY, 'space_before': 6}),
], size=10, line_spacing=1.1, space_after=8)
rect(s, rx_, BODY_Y + 0.05, cw2, 0.6, fill=BLUE)
text(s, rx_ + 0.2, BODY_Y + 0.05, cw2 - 0.4, 0.6, "REBUILD AI-NATIVELY  —  as a new parallel stack", size=11, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
rect(s, rx_, BODY_Y + 0.65, cw2, 3.2, fill=PALE)
text(s, rx_ + 0.25, BODY_Y + 0.85, cw2 - 0.5, 3.0, [
    ("**The interface and conversational layer** — the Analyst", {'bullet': True}),
    ("**The agent and recommendation layer** — the Decision Feed", {'bullet': True}),
    ("**Reporting** — the Fleet P&L", {'bullet': True}),
    ("**Onboarding and configuration** — schema mapping, car-group normalisation, seasonality inference", {'bullet': True}),
    ("**Support** — tier one, multilingual", {'bullet': True}),
    ("**The coach's own workflow** — diagnostic sequence, pace reading, station reviews", {'bullet': True}),
    ("This is the part that became dramatically cheaper in the last two years — and the part WeYield lacks.", {'italic': True, 'color': NAVY, 'space_before': 6}),
], size=10, line_spacing=1.1, space_after=6)
rect(s, ML, BODY_Y + 4.0, W - ML - MR, 1.0, fill=NAVY)
text(s, ML + 0.25, BODY_Y + 4.0, W - ML - MR - 0.5, 1.0,
     "**The discipline that makes it work without a migration project:** from day one every new feature ships in the new stack. **The old stack receives no new features, ever — maintenance only.** Over eighteen months the new stack absorbs 60–70% of user-facing surface, and the old one shrinks by attrition rather than by decision.",
     size=10.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.12, space_after=0)

# ---------- 14. Data assets ----------
s = new_slide("The moat is the combination of three data sets that no one else holds for this segment",
              tracker="3 · The recommendation",
              source="Source: WeYield product footprint per weyield.io and The AI Turn for WeYield (Sep 2026); ForwardKeys embedding and IATA exploration per Olivier Jager, 10 Sep 2026. Indicata (Autorola) and Autovista are named as candidate partners, not confirmed counterparties.")
table(s, ML, BODY_Y + 0.05, 8.3, [
    ["Data asset", "Status", "Action"],
    ["**Cross-tenant rate shop, pace, utilisation and fleet** — years of history across 50+ countries and multiple operating models", "HELD", "Instrument at daily grain per account. Verify 24-month reconstructability. This is the moat; everything else is a feature."],
    ["**Forward demand signal** — ForwardKeys embedded; IATA under exploration as Amadeus repricing bites", "HELD", "Deepen. Olivier's own background in this data is an asset to use."],
    ["**Used-vehicle residual data** — by market, model, specification, mileage, age", "MISSING", "**Partnership, not modelling.** Indicata is the strongest single candidate; Autovista for forecasts; BCA / Manheim for auction. On the critical path for Horizon 2."],
    ["**Recommendation accept / modify / reject telemetry** — with subsequent RPD and utilisation outcome", "UNKNOWN — verify", "Turn on immediately. Cheap today; impossible to backfill. Without it there is no agent that learns and no outcome price that can be defended."],
], col_w=[3.3, 1.35, 3.65], size=9.5, row_h=0.9, status_col=1)
callout(s, 9.05, BODY_Y + 0.05, 3.78, 2.45, "The defensible statement of the moat",
        ["**Forward demand + realised pace + used-vehicle residuals.** Nobody holds all three for the long tail.",
         "A foundation model cannot acquire it. A funded newcomer cannot buy it. A PMS vendor sees only its own base."], body_size=10)
callout(s, 9.05, BODY_Y + 2.65, 3.78, 2.35, "What a customer cannot rebuild with AI",
        ["Olivier's threat — a customer rebuilds the tool and cancels — is real for the feature layer. It is not real for cross-tenant benchmarks, forward demand, or the integration lattice. **Make the data and the network the product; let the features commoditise.**"],
        fill=BG2, accent=GREY, body_size=9.5)

# ---------- 15. Three horizons ----------
s = new_slide("Three horizons, each funding the next — the plan requires no external capital",
              tracker="4 · The plan",
              source="Note: Emmanuel has flat EBITDA, no cash reserve and no raise in progress. Any plan that requires new capital will be received politely and shelved. Revenue and ACV milestones are illustrative (slide 17).")
hz = [
    ("Horizon 1", "Months 0–6", "Repair the economics", "EBITDA ~0% → ~25% without touching the roadmap", [
        "**Validate first** — ten customer calls against the three kill-risks. Gates everything.",
        "**Reprice the top 20** onto a per-vehicle model. ~95% incremental margin, zero code.",
        "**AI inside the company** — support, onboarding, config, QA, coaching prep.",
        "**Ship the Analyst** — two-week build, two-person pod. Proves the cost thesis.",
        "**Instrument the loop** — accept / modify / reject + outcome.",
        "**Write the coaching methodology** as specification — the training corpus."], NAVY),
    ("Horizon 2", "Months 6–18", "Change the object and the buyer", "Revenue €1.95M → €3.2M · ACV €16K → €22K", [
        "**Close the residual-data partnership** — Indicata or equivalent. Critical path.",
        "**Ship the Fleet P&L** — the owner's report. Changes the buyer.",
        "**Ship the Decision Feed** across five levers, guardrailed and logged.",
        "**Move the pricing model** — base + per-vehicle + outcome-linked where attribution holds.",
        "**Hire salespeople 3 and 4** — only now, at ~12-month payback."], BLUE),
    ("Horizon 3", "Months 18–36", "Compound the data", "Revenue ~€4.8M at 30%+ EBITDA · a genuine strategic option", [
        "**Cross-tenant benchmarking as a product** — “comparable operators are holding rates 4% above you into half-term.”",
        "**Answer-layer monitoring** — does your customer appear in the AI assistants, at what rate, in what class, still bookable? Nobody sells this.",
        "**Re-scope the coach** from analyst to supervisor of agents across 5× the accounts — the gross-margin unlock."], NAVY),
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
text(s, ML + 0.2, BODY_Y + 4.55, W - ML - MR - 0.4, 0.45, "Sequence: Price → Cost → Sell → Build.   Q1 repricing and cost-to-serve fund the Q2 pod; the pod's savings fund the Q3–Q4 hires; the hires fund Year 2. Emmanuel never has to ask anyone for money.",
     size=9.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, space_after=0)

# ---------- 16. Organisation ----------
s = new_slide("Headcount grows 9 → 16 while revenue triples — the decoupling comes from not hiring, never from cutting",
              tracker="4 · The plan",
              source="Note: current function split (~5 product/engineering, 2 sales, 2 other) is inferred from the reported 9 employees and 2 salespeople and must be confirmed. Target shape aligns to the illustrative Year-3 plan on slide 17.")
table(s, ML, BODY_Y + 0.05, 8.2, [
    ["Function", "Today", "Target (Year 3)"],
    ["**Product / engineering**", "~5, building features with unproven ROI", "3–4 on integrations, data pipeline and the numeric core — the part never rewritten, and the highest-skill work in the company"],
    ["**AI-native pod**", "0", "2–3 forward-deployed engineers owning interface, agents and onboarding"],
    ["**Sales**", "2", "4–5 — hired only once ACV supports a ~12-month payback"],
    ["**Coaching**", "Analysts", "Fleet advisors supervising agents across 5× the accounts"],
    ["**Data partnerships**", "0", "1 — owns Indicata, IATA, and the benchmark product"],
    ["**Total**", "**9**", "**~16**"],
], col_w=[1.9, 2.3, 4.0], size=9.5, row_h=0.62, bold_first_col=False)
callout(s, 8.95, BODY_Y + 0.05, 3.88, 2.5, "The French constraint — raise it before he does",
        ["Five engineers cannot simply be cut. *Licenciement économique* is slow, expensive, needs documented justification, and signals distress to customers and acquirers alike.",
         "So the cost decoupling comes from **not hiring**. The nine stay; the next nine are never hired; the work doubles."], body_size=9.5)
rect(s, 8.95, BODY_Y + 2.7, 3.88, 2.3, fill=NAVY)
text(s, 9.15, BODY_Y + 2.82, 3.5, 0.3, "The framing that is also true", size=9, color=LBLUE, bold=True, space_after=0)
text(s, 9.15, BODY_Y + 3.15, 3.5, 1.8, [("“The engineers are not the problem. They are on the wrong side of the line. Move them onto the moat.”", {'size': 12.5, 'color': WHITE, 'font': SERIF, 'space_after': 8}),
                                          ("WeYield stops being a company that ships features and becomes a company that ships decisions: *we recommended Y, the customer accepted it, and it was worth €Z.*", {'size': 9, 'color': LBLUE})], line_spacing=1.1)

# ---------- 17. Three-year shape ----------
s = new_slide("Illustrative three-year shape — revenue ×3.2, EBITDA to ~31%, and a valuation of €19–24M against ~€2M today",
              tracker="5 · Economics and risk", sticker="Illustrative",
              source="Assumptions, not verified: cost base ~€1.4M; people ~€1.0–1.05M; ~5 of 9 heads in engineering; top-20 accounts ≈ 50% of revenue; per-vehicle repricing on renewal; fleet module attach at 30 of the top accounts in Y2. Valuation multiple indicative for vertical SaaS above Rule of 40. Do not circulate externally in this form.")
text(s, ML, BODY_Y, 6.4, 0.3, "Revenue, €M — with EBITDA margin", size=11, color=NAVY, bold=True)
vcols(s, ML, BODY_Y + 0.4, 6.4, 4.4, [
    ("Today", 1.5, MID), ("Year 1", 1.95, LBLUE), ("Year 2", 3.2, BLUE), ("Year 3", 4.8, NAVY),
], max_val=5.6, fmt=lambda v: f"€{v:g}M", top_labels=["~0% EBITDA", "~26%", "~28%", "~31%"], value_size=12)
table(s, 7.3, BODY_Y + 0.05, 5.53, [
    ["", "Today", "Year 1", "Year 2", "Year 3"],
    ["Customers", "120", "125", "150", "190"],
    ["Blended ACV", "€12.5K", "€16K", "€22K", "€26K"],
    ["Revenue", "€1.5M", "€1.95M", "€3.2M", "€4.8M"],
    ["EBITDA margin", "~0%", "~26%", "~28%", "~31%"],
    ["Growth", "10–15%", "30%", "64%", "50%"],
    ["Rule of 40", "~15", "~56", "~92", "~81"],
    ["Headcount", "9", "10", "13", "16"],
    ["**Indicative valuation**", "**€2M (1.3×)**", "—", "—", "**€19–24M (4–5×)**"],
], col_w=[1.45, 1.05, 0.95, 0.95, 1.13], size=9, row_h=0.36, header_size=9,
      col_align=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT, PP_ALIGN.RIGHT])
callout(s, 7.3, BODY_Y + 3.5, 5.53, 1.1, None,
        ["**€2M on €1.5M is 1.3× — the correct price for 15% growth at zero margin.** The offer measures the operating model. Both credible end-states, independence or sale, run through the same eighteen months of work."],
        fill=BG2, accent=NAVY, body_size=9.5)

# ---------- 18. Growth from ACV ----------
s = new_slide("Growth comes from ACV, not logos — customers +58%, ACV +108%, revenue +220% over three years",
              tracker="5 · Economics and risk", sticker="Illustrative",
              source="Source: illustrative plan on slide 17. Percentages are Year-3 vs today. Headcount growth of +78% against revenue growth of +220% is the cost/revenue decoupling identified as the objective in Olivier Jager's review of 10 Sep 2026.")
text(s, ML, BODY_Y, 7.6, 0.3, "Change from today to Year 3, %", size=11, color=NAVY, bold=True)
hbars(s, ML, BODY_Y + 0.55, 7.6, [
    ("Customers", 58, MID, "+58%"),
    ("Headcount", 78, MID, "+78%"),
    ("Blended ACV", 108, LBLUE, "+108%"),
    ("Revenue", 220, BLUE, "+220%"),
], max_val=250, label_w=1.8, bar_h=0.5, gap=0.38, label_size=10.5)
callout(s, 8.6, BODY_Y + 0.05, 4.23, 1.75, "The case against hiring salespeople first",
        ["Customers grow 58% over three years; revenue grows 220%. **The growth is in the price and the buyer, not the logo count.** That is the entire argument for changing the object before expanding the sales team."], body_size=10)
callout(s, 8.6, BODY_Y + 2.0, 4.23, 1.95, "The decoupling Olivier asked for",
        ["Headcount +78% against revenue +220%. Cost no longer scales with sales — achieved by *not hiring*, which is the only version available under French employment law.",
         "Every EBITDA point of that gap is what moves the exit number."], fill=BG2, accent=GREY, body_size=9.5)

# ---------- 19. Kill-risks ----------
s = new_slide("Three facts would kill the thesis — all are testable within two weeks and should gate every line of code",
              tracker="5 · Economics and risk",
              source="Note: kill-risk 3 uses the same fleet-size-by-account data required for the Horizon 1 repricing exercise, so the test costs nothing additional. A plan without these tests is a pitch.")
table(s, ML, BODY_Y + 0.05, W - ML - MR, [
    ["Kill-risk", "Why it kills the thesis", "The test", "If it fails"],
    ["**1 · Buyback exposure**", "Customers still on OEM buyback or guaranteed repurchase do not own residual risk. The Fleet P&L then has no buyer.", "Ten customer calls: what share of the fleet is on buyback, on operating lease, owned at risk — and how has that mix moved since 2021?", "Thesis narrows to the owned-at-risk segment. Size it before proceeding. The move and substitute levers remain valid regardless."],
    ["**2 · Fleet financials unreachable**", "Fleet counts and utilisation already flow into Performance Hub and Revenue Horizon (per the site). The open question is the *financial* fields: if acquisition cost, in-service date, mileage and disposal are absent from the integrated PMSs, the product becomes data entry, which is not adopted.", "Field-coverage audit across the five most common PMS integrations in the installed base.", "First release becomes a fleet-data ingestion product. Timeline extends six to nine months."],
    ["**3 · Fleet-size distribution**", "If the median customer fleet is under ~200 vehicles, de-fleet decisions are too lumpy to optimise and value per account will not support the ACV step-up.", "Fleet size by account across the base — the same data as the repricing exercise. Zero incremental cost.", "The fleet product is a top-quartile offer, not a platform offer. Still a viable business; a different one, with a different sales model."],
], col_w=[2.1, 3.7, 3.35, 3.18], size=9.5, row_h=1.15)
rect(s, ML, BODY_Y + 4.35, W - ML - MR, 0.65, fill=NAVY)
text(s, ML + 0.25, BODY_Y + 4.35, W - ML - MR - 0.5, 0.65, "**The honest uncertainty in this plan sits in kill-risk 1.** The direction of the post-2021 buyback contraction is well established; its magnitude in WeYield's specific base of island, leisure and Eastern European franchisees is not. That is the hinge the thesis turns on — and it is one week of calls away.",
     size=10, color=WHITE, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.1, space_after=0)

# ---------- 20. Six decisions ----------
s = new_slide("Six decisions for Monday",
              tracker="5 · Economics and risk",
              source="Note: decisions 1 and 2 are diagnostic and cost nothing; 3 and 5 are policy changes with immediate effect; 4 is the first spend (~€30–50K over the quarter); 6 is a commercial conversation whose lead time exceeds any integration.")
decs = [
    ("Commission the ten-call validation", "Buyback exposure, PMS fleet-data coverage, fleet-size distribution. Everything else is gated on this.", "Emmanuel", "Week 1"),
    ("Pull the fleet size behind every top-20 account", "Run $4 / $6 / $8 per vehicle per month against them. If those numbers cannot be produced, that is itself the most important finding of the week.", "Head of sales", "Week 1"),
    ("Freeze the old stack", "No new features, effective immediately. Maintenance only.", "CTO", "Immediate"),
    ("Stand up the two-person AI-native pod", "First delivery: the Analyst, on a two-week clock. Its second purpose is to prove the delivery-cost thesis to the board.", "Emmanuel / CTO", "Week 2"),
    ("Turn on recommendation telemetry", "Accept, modify, reject — and the outcome. Cheap today, impossible to reconstruct later.", "Engineering", "Week 2"),
    ("Open the Indicata conversation", "On the critical path for Horizon 2. Commercial negotiations take longer than integrations.", "Emmanuel", "Week 2"),
]
yy = BODY_Y + 0.05
for i, (hd, body, owner, when) in enumerate(decs):
    rect(s, ML, yy, 0.55, 0.72, fill=NAVY if i not in (0, 1) else BLUE)
    text(s, ML, yy, 0.55, 0.72, str(i + 1), size=18, color=WHITE, font=SERIF, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    rect(s, ML + 0.55, yy, W - ML - MR - 0.55, 0.72, fill=BG2 if i % 2 == 0 else WHITE, line=None)
    text(s, ML + 0.75, yy + 0.06, 3.3, 0.6, hd, size=11, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.0, space_after=0)
    text(s, ML + 4.15, yy + 0.06, 5.6, 0.6, body, size=9.5, color=INK, anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.08, space_after=0)
    text(s, ML + 9.85, yy + 0.06, 1.25, 0.6, owner, size=9, color=GREY, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(s, ML + 11.15, yy + 0.06, 1.08, 0.6, when, size=9, color=NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT, space_after=0)
    hline(s, ML + 0.55, yy + 0.72, W - ML - MR - 0.55, color=RULE)
    yy += 0.78
text(s, ML + 0.75, BODY_Y - 0.02, 3, 0.25, "DECISION", size=7.5, color=GREY, bold=True, space_after=0)
text(s, ML + 9.85, BODY_Y - 0.02, 1.25, 0.25, "OWNER", size=7.5, color=GREY, bold=True, space_after=0)
text(s, ML + 11.15, BODY_Y - 0.02, 1.08, 0.25, "WHEN", size=7.5, color=GREY, bold=True, align=PP_ALIGN.RIGHT, space_after=0)
text(s, ML, BODY_Y + 4.78, W - ML - MR, 0.3, "The real risk is not choosing the wrong AI strategy. It is spending 2027 deciding.", size=12, color=NAVY, font=SERIF, align=PP_ALIGN.CENTER, space_after=0)

# ---------- 21. Appendix ----------
s = new_slide("Appendix — every figure in this document is given, derived or assumed; none is verified against WeYield's accounts",
              tracker="Appendix",
              source="Source: Olivier Jager, strategic review (CR_reunion_WeYield, 10 Sep 2026) and briefing call of the same date; The AI Turn for WeYield (Sep 2026). Prepared by Ram Badrinathan, September 2026.")
table(s, ML, BODY_Y + 0.05, W - ML - MR, [
    ["Category", "Figures", "Treatment"],
    ["**Given**", "€1.5M revenue · ~120 customers · 9 employees, 2 in sales · 600–1,000 addressable · 10–15% growth · EBITDA flat/contracting · ~€2M standing offer · 2–3 year exit intent · 4% industry net margin · average deal “under €40K” · +6% RPD at Aircar", "As reported by Olivier Jager, 10 September 2026. Not independently verified."],
    ["**Derived**", "€12.5K implied ACV · 12–20% penetration · €7.5–12.5M TAM at current ACV · 1.3× revenue multiple · Rule of 40 ≈ 15 · ~€85K new ARR per rep", "Arithmetic on the given figures only."],
    ["**Assumed**", "Cost base ~€1.4M · people ~€1.0–1.05M · ~5 of 9 heads in engineering · €90K loaded rep cost · €700 RPU/month · €15K disposal value · 20/100 account distribution · all Year 1–3 projections · indicative multiple ranges", "**Not verified.** Must be checked against WeYield's accounts before any external use."],
    ["**Unresolved**", "“Average deal under €40,000” vs €12,500 implied · 600 vs 600–1,000 addressable · “120 customers” vs “100+ users” · identity of the ~€2M acquirer", "Flagged for confirmation on the call. **Probable reconciliation of the first:** ~20 accounts at €35–40K ≈ half of revenue; ~100 accounts at €7–8K ≈ the other half. If so, both figures are true — and the repricing opportunity is concentrated in 20 accounts."],
], col_w=[1.5, 6.4, 4.43], size=9.5, row_h=0.95)

prs.save(OUT)
print("WROTE", OUT, "slides:", len(prs.slides))
