# WeYield — AI-Native Advisory Pack

**Live site:** https://weyield-advisory.vercel.app

A deck and five documents on how WeYield becomes AI-native — not by adding features, but by
changing what it sells, who it sells to, and what it costs to serve them.

Prepared for **Emmanuel Scuto** by **Ram Badrinathan**, September 2026, following the strategic
review of 10 September 2026.

> **Confidential.** This repository is private. It contains figures about WeYield's business.
> Please don't make it public or fork it to a public account.

---

## Start here

| | Document | Answers |
|---|---|---|
| 📊 | **[The deck](https://weyield-advisory.vercel.app/deck)** — 21 slides, ~15 min | The whole argument, compressed |
| 1 | **[Five Moves](https://weyield-advisory.vercel.app/five-moves)** | What is actually wrong, and the five things to do about it |
| 2 | **[Monday Brief](https://weyield-advisory.vercel.app/monday-brief)** | What ships first, and exactly how it works |
| 3 | **[Residual Radar](https://weyield-advisory.vercel.app/residual-radar)** | Where the profit really sits, and where the used-car data comes from |
| 4 | **[Agentic GTM](https://weyield-advisory.vercel.app/agentic-gtm)** | How nine people reach six hundred operators |
| 5 | **[Tech Stack](https://weyield-advisory.vercel.app/tech-stack)** | What two engineers build it on |

**The fastest way to help:** open [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md). It collects every
assumption and open question from across the pack into one list. Answering even half of them
would change several of the conclusions.

---

## What this is, and what it is not

**It is** a first pass, written quickly, to give you something concrete to react to.

**It is not** a diligence exercise. Nothing here has been verified against WeYield's accounts or
systems, and there is no financial model behind it. Product facts come from weyield.io and the
September review; everything else is derived arithmetic or a stated assumption. Anything marked
*illustrative* in a caption is the shape of an argument, not a projection.

Several conclusions rest on three facts I could not check — they're the first three rows of
[`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md), and if any of them is different from what I assumed,
a good part of the argument changes.

---

## How to contribute

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Three ways, easiest first:

1. **Answer the open questions** — edit `OPEN-QUESTIONS.md` in the browser, no tooling needed
2. **Open an issue** — for anything that's wrong, missing, or worth arguing about
3. **Edit the documents** — `source/pages/*.html`, then rebuild

You do not need to know git or HTML to be useful here. Answering the questions is the valuable part.

---

## Repository layout

```
/                          the built site — this is what Vercel serves
  index.html               hub
  deck.html                21-slide viewer
  five-moves.html …        the five documents
  slides/                  deck slide images (WebP)
  vercel.json

source/                    editable originals — edit these, not the built files
  pages/                   the five documents, before the site wrapper is added
  docs/                    markdown sources
    strategy.md              the full strategy write-up
    monday-brief-spec.md     the Monday Brief product specification
    meeting-record-*.md      the 10 Sep review, translated to English
  deck/                    the deck as .pptx
  build/                   scripts that regenerate the site from source/
```

### Rebuilding the site

The files at the repository root are **generated**. Edit `source/pages/`, then:

```bash
python source/build/build_site.py        # rebuilds hub + the five pages
python source/build/build_deck_page.py   # rebuilds the deck viewer
```

Both scripts have absolute paths at the top that need pointing at your own checkout.
Then deploy with `vercel --prod`, or just push and let Vercel do it if git integration is on.

---

## Companion documents

Editable in Google, comments welcome:

- [Building the AI-Native Business](https://docs.google.com/document/d/1iQSuJYMgsaXIxJb6D2mAlHmENs-kCT6BQcEkIkl9UL8/edit) — the full strategy
- [Strategy deck, 21 slides](https://docs.google.com/presentation/d/1-tBUAFx9sy_matkUt6UWys64sCcNvBaI3-guEI2WtqM/edit) — the editable original
- [Meeting record, 10 Sep 2026](https://docs.google.com/document/d/1aC1ShK6GCExt4E5apfbiB5vMhe9qAwxPBI7mawjeKfM/edit) — translated to English

---

*Everything in this pack is written to be argued with.*
