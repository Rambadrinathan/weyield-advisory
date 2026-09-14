# Open questions and assumptions

**Updated 14 September 2026, after our conversation of 13 September.** Nine questions are now
answered — struck through with your answer recorded. Twelve remain, plus five new ones the call
raised.

**How to use this:** type into the *Answer* column. No tooling, no git knowledge — edit it in the
browser (the pencil icon, top right of this file on GitHub), or reply by email and I'll fill it in.

Rows marked 🔴 are **kill-risks**: if the answer differs from what I assumed, a substantial part of
the argument stops working.

---

## 🔴 The three that gate everything

| # | Question | What I assumed | Status | Answer |
|---|---|---|---|---|
| 1 | What share of your customers' fleets is on **OEM buyback / guaranteed repurchase**, versus operating lease, versus owned at risk? How has that mix moved since 2021? | That a meaningful and growing share is owned at risk | **In progress.** You have been discussing the car question with customers for two days and will continue. Ten structured calls finishes it. | |
| 2 | Do **acquisition cost, in-service date, mileage, specification and disposal** reach the PMS systems you integrate with? | That some do, patchily | **More worrying after the call.** You described the ERPs as slow and unsophisticated, serving unsophisticated buyers. Assume the fields are thin until proven otherwise. | |
| 3 | What is the **median fleet size** across the base, and the distribution? | A long tail below 300 cars | **Open, and now more material.** With ten-car and fifty-car operators in the base, the distribution decides whether the fleet product is a platform or a top-quartile offer. | |

---

## ✅ Answered on 13 September

| # | Question | Your answer | What it changed |
|---|---|---|---|
| ~~5~~ | Addressable market — 600 or 1,000? | **~1,000** workable, 100+ customers | Penetration is ~10%. TAM arithmetic redrawn. |
| ~~6~~ | 120 customers vs "100+ users" | **"100 plus"** paying customers | Per-account figures rebased |
| ~~8~~ | Do coaches write weekly notes today? | Better than notes — **three years of every consultant call, recorded with consent**, now the training corpus | This is the moat. Deck slide 3 is about nothing else. |
| ~~12~~ | Which markets read WhatsApp rather than email? | Partially — the base is **worldwide, not Europe-centric** | Weakens the Europe-only LEZ analysis; raises multilingual priority |
| ~~19~~ | Is growth new logos or expansion? How many logos per rep? | One salesperson hired 10 months ago, **8 months to ramp**; before that you were the only seller | Rep-payback maths holds; the constraint is even tighter than modelled |
| ~~22~~ | Do you have ISO 27001, or has a customer asked? | Not raised — **still open**, see new question 31 | — |
| ~~23~~ | What is the current stack? | **Christian, PhD maths/CS**, self-hosted 3B fine-tune, no external tokens | Version 1's frontier-model recommendation withdrawn for the daily summary |
| ~~25~~ | Where do you host, and in which region? | **Your own infrastructure** — "we don't buy any tokens because it's on our side" | Data sovereignty is already solved. A real advantage. |
| ~~26~~ | How is the engineering team split? | 9 people, Christian CTO, product-led culture — *"a product mindset type of team who love developing features"* | Confirms the diagnosis; organisation slide rewritten |

---

## Still open — Monday Brief and the agent

| # | Question | Why it matters | Answer |
|---|---|---|---|
| 7 | Does **Performance Hub** expose a per-account API or warehouse at **station × car group × day** grain? | Decides whether the facts layer is four weeks or twelve | |
| 9 | How many accounts run **all three** of Market Radar, Performance Hub and Revenue Horizon? | The brief degrades gracefully without one, but the richest version assumes all three | |
| 10 | Which **six languages** cover ~90% of recipients, now we know the base is worldwide? | A 3B fine-tune will be weakest exactly here — it decides where a frontier model earns its cost | |
| 11 | Do current customer contracts permit **cross-tenant benchmarking**? Who reviews? | Gates the benchmark product. Note: self-hosting removes the sub-processor question entirely. | |
| 13 | Which are the **top 20 accounts by ACV**? | Same list the repricing exercise needs | |
| 14 | Do **idle-unit counts and station fleet plans** already reach Performance Hub? | The transfer rule depends on it | |

---

## New questions the call raised

| # | Question | Why it matters | Answer |
|---|---|---|---|
| 27 | **What does the daily summary get wrong** in the 3–5%? Arithmetic, judgement, or confident invention? | Decides whether the verifier is mostly numeric checking or needs a judgement layer too. **The single most useful thing you could tell me.** | |
| 28 | Are customers **paying** for the daily summary, or is it bundled into the existing subscription? | Whether this is already a product or still a feature | |
| 29 | Can Christian **read out** what the model learned — or is the method only in the weights? | If it is only in the weights: no audit, no correction, no handover. This is a succession issue as much as a product one. | |
| 30 | Of the operations pain you described — cars back in the wrong place, damaged, not ready to re-rent — **which one costs the most**? | You said you have to "enter into the operation". This decides where. | |
| 31 | Has a **franchisor or large network** ever asked you for ISO 27001 or a security review? | Certification takes 6–12 months and would block the largest deal at the worst moment | |
| 32 | **Exit horizon** — you said five to six years, to your two C-levels. Olivier's note said two to three, and a sale. Which is the plan? | These optimise for genuinely different things. Worth settling. | |

---

## Still open — Residual Radar

| # | Question | Why it matters | Answer |
|---|---|---|---|
| 15 | Do you already capture **disposal records** — date, vehicle, mileage, channel, price achieved? | The proprietary asset. Costs almost nothing to start; **cannot be backfilled.** | |
| 16 | Any existing relationship with **Indicata, Autovista, cap hpi, BCA or Manheim**? | Turns a cold procurement conversation into a warm one | |
| 17 | Your base is worldwide — **which markets have no used-vehicle price source at all**? | European providers will not cover much of your footprint. This shapes the partnership. | |
| 18 | What is the actual **powertrain mix** across the base? | The sensitivity ranking inverts between a diesel-heavy and an EV-heavy fleet | |

---

## Still open — go to market

| # | Question | Why it matters | Answer |
|---|---|---|---|
| 20 | How many of the 100+ accounts are **RM consultants** serving several operators, and how many operators sit behind them? | The fastest one-to-many route, and probably under-weighted | |
| 21 | Any existing **franchisor relationship** at group or regional level? | 9–18 month lead time, so warm contacts change the plan | |
| 33 | What does the **market-trends lead magnet** actually convert at? | You already run the mechanism the AI audit would extend. Its baseline sets the target. | |
| 24 | Can the existing product expose a **scheduled data extract** and an **API for write-back**? | Everything in the architecture note assumes both | |

---

## Assumptions I made up entirely

Not questions — numbers I invented to make a mechanism visible, each marked *illustrative* where
it appears. **Correct any and the relevant exhibit should be redrawn.**

| Assumption | Value used | Where it appears |
|---|---|---|
| Operator revenue per unit per month | €700 | Residual Radar, Five Moves |
| Average vehicle acquisition cost | €22,000 | Residual Radar |
| Average disposal value at 24 months | €14,000 | Residual Radar |
| Operator net margin | 4% *(Olivier's figure, not mine)* | Throughout |
| Share of operator cost that is the car | **60–70%** *(yours, 13 Sep — now load-bearing)* | Deck slides 7, 8 |
| Ancillary share of revenue | 25–35% | Five Moves |
| Ancillary contribution margin | 80–90% | Five Moves |
| Fully loaded salesperson cost | €90,000 | Agentic GTM, Five Moves |
| Cost to serve, human onboarding | €13,000 / account / year | Five Moves |
| Cost to serve, agent onboarding | €1,500 / account / year | Five Moves |
| Model inference cost per brief | €0.12–0.20 | Monday Brief spec — **now wrong for you.** Your marginal cost is zero. |

---

## Anything else

| From | Note | |
|---|---|---|
| | | |
