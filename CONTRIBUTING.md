# How to contribute

You do not need to know git or HTML to be useful here. In order of how much they help:

## 1. Answer the open questions  ← the valuable one

Open [`OPEN-QUESTIONS.md`](OPEN-QUESTIONS.md), click the pencil icon at the top right, type into
the *Answer* column, and press **Commit changes**. GitHub handles the rest — nothing to install.

The three rows marked 🔴 are worth more than everything else on this list combined. They are the
facts that would collapse a substantial part of the argument if they turn out differently, and
ten customer calls settles all three.

## 2. Open an issue

For anything wrong, missing, or worth arguing about. Use the **Issues** tab, or the templates:

- **Correct a fact or assumption** — for a figure, claim or assumption that is wrong
- **Add context** — for something the analysis is missing entirely
- **Challenge a conclusion** — for where the reasoning does not hold

Disagreement is the point. A note saying *"this is wrong because…"* is worth more than a correction
without a reason.

## 3. Edit the documents directly

The HTML files at the repository root are **generated** — do not edit them, they get overwritten.

Edit `source/pages/*.html` instead, then rebuild:

```bash
python source/build/build_site.py
python source/build/build_deck_page.py
```

Both scripts have absolute paths at the top that need pointing at your own checkout. Commit both
the source change and the rebuilt output.

For the markdown documents under `source/docs/`, edit directly — they are not generated from
anything.

## 4. Just reply by email

Entirely fine. Send it and I will fold it in.

---

## A note on the numbers

Nothing in this pack has been verified against WeYield's accounts or systems. Where a figure is
yours it comes from the 10 September review or from weyield.io; everything else is derived
arithmetic or an assumption I made explicit. The table at the end of `OPEN-QUESTIONS.md` lists
every invented number and where it appears.

Correcting one of those is not a small contribution — several exhibits change with them.
