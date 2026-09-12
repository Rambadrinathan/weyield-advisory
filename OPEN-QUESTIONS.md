# Open questions and assumptions

Every question and unverified assumption from across the pack, in one place.

**How to use this:** type your answer in the *Answer* column. That's it — no tooling, no git
knowledge. Edit it in the browser (the pencil icon, top right of this file on GitHub), or just
reply by email and I'll fill it in.

Rows marked 🔴 are **kill-risks** — if the answer differs from what I assumed, a substantial part
of the argument stops working. Those three are worth ten customer calls this week, before anything
is built.

---

## 🔴 The three that gate everything

| # | Question | What I assumed | Why it matters | Answer |
|---|---|---|---|---|
| 1 | What share of your customers' fleets is on **OEM buyback / guaranteed repurchase**, versus operating lease, versus owned at risk? And how has that mix moved since 2021? | That a meaningful and growing share is owned at risk | If operators don't carry residual risk, the Fleet P&L product has no buyer and *Residual Radar* narrows to a segment that needs sizing first | |
| 2 | Do **acquisition cost, in-service date, mileage, specification and disposal** actually flow into the PMS systems WeYield integrates with? (Fleet *counts* and utilisation clearly do — this is about the financial fields) | That some do, patchily | If they don't, the first release becomes a fleet-data ingestion product and the timeline extends 6–9 months | |
| 3 | What is the **median fleet size** across the customer base, and the distribution? | A long tail below 300 cars with a top tier well above | Below ~200 cars, de-fleet decisions are too lumpy to optimise and the value per account won't support the ACV step-up | |

---

## Numbers I could not reconcile

Three figures in my source material contradict each other. I've flagged rather than guessed.

| # | The conflict | Why it matters | Answer |
|---|---|---|---|
| 4 | Average deal size was described as "under €40,000", but revenue ÷ customers implies roughly €12,500. My guess is that €40K describes the **top tier** and €12.5K is the mean — perhaps ~20 accounts at €35–40K and ~100 at €7–8K? | The whole repricing argument depends on the actual ACV distribution | |
| 5 | Addressable market is given as **600** in one place and **600–1,000** in another | Penetration is either 12% or 20%; the TAM ceiling moves by €5M | |
| 6 | "**120 customers**" versus "100+ **users** across 50+ countries" — how many are paying accounts, and how many are seats? | Every per-account figure in the pack | |

---

## Monday Brief — before week one

| # | Question | Why it matters | Answer |
|---|---|---|---|
| 7 | Does **Performance Hub** expose a per-account API or warehouse at **station × car group × day** grain — RPD, utilisation, bookings, pace, fleet counts, idle days? | This decides the eight-week timeline. If not, week 1 becomes a data-access sprint | |
| 8 | Do coaches write **weekly notes** for accounts today? How many accounts, and in what form? | These are the style exemplars for the composer. Without them the Academy material substitutes and tone review takes longer | |
| 9 | How many accounts run **all three** of Market Radar, Performance Hub and Revenue Horizon? | The brief degrades gracefully without one, but the richest version assumes all three | |
| 10 | Which **six languages** cover ~90% of recipients? | Multilingual is nearly free, but the style guide needs exemplars per language | |
| 11 | Do current customer contracts permit an **LLM sub-processor**, and **opt-in cross-tenant benchmarking**? Who reviews? | Gates the benchmark block and, in principle, the whole product | |
| 12 | In which markets do owners read **WhatsApp** rather than email? | Islands, North Africa and Latin America are my guess — worth confirming per region | |
| 13 | Which are the **top 20 accounts by ACV**? | Same list the repricing exercise needs, and it defines the tier-A coach-review path | |
| 14 | Do **idle-unit counts and station fleet plans** already reach Performance Hub, as the site copy implies? | Rule R3 (idle-vs-shortfall transfers) depends on it | |

---

## Residual Radar — the data question

| # | Question | Why it matters | Answer |
|---|---|---|---|
| 15 | Do you already capture **disposal records** from customers — date, vehicle, mileage, channel, price achieved? | This is the proprietary asset. It costs almost nothing to start capturing and **cannot be backfilled** — every month of delay is a month of history that never exists | |
| 16 | Any existing relationship with **Indicata, Autovista, cap hpi, BCA or Manheim**? | Changes a cold procurement conversation into a warm one, and the barter framing needs a starting point | |
| 17 | For your **island, North African and New Zealand** markets — is there any used-vehicle price source at all? | I have no basis to assume the European providers cover these, and they're a distinctive part of your footprint | |
| 18 | What is the actual **powertrain mix** across the customer base — diesel, petrol, hybrid, BEV? | The sensitivity ranking inverts completely between a diesel-heavy Mediterranean fleet and an EV-heavy Nordic one | |

---

## Go-to-market

| # | Question | Why it matters | Answer |
|---|---|---|---|
| 19 | Is the 10–15% growth **new logos or expansion**? How many new logos per salesperson per year? | I assumed ~7 per rep. If it's expansion-led, the entire GTM argument changes shape | |
| 20 | How many of the ~120 accounts are **RM consultants** serving several operators, and how many operators sit behind them? | The consultant channel is the fastest one-to-many route and I may be under-weighting it | |
| 21 | Any existing **franchisor relationship** at group or regional level? | Network Edition is the largest move and its lead time is 9–18 months, so warm contacts change the plan | |
| 22 | Do you have **ISO 27001** or SOC 2, or has a customer ever asked? | Franchisor procurement will ask. Certification takes 6–12 months and would otherwise block the biggest deal at the worst moment | |

---

## Technology

| # | Question | Why it matters | Answer |
|---|---|---|---|
| 23 | **What is the current stack?** Language, framework, database, hosting. | I wrote the architecture note without knowing this. The recommendation is additive either way, but I'd like to stop guessing | |
| 24 | Can the existing product expose a **scheduled data extract** and an **API for write-back**? | Everything in the architecture note assumes both. If neither exists, that's week one | |
| 25 | Where does the product **host** today, and in which region? | Decides whether in-region model inference is a small step or a migration | |
| 26 | Roughly how is the engineering team **split** across product, integrations and support? | I assumed ~5 of 9 in engineering. The cost arithmetic moves with it | |

---

## Assumptions I made up entirely

These are not questions — they are numbers I invented to make a mechanism visible. Each is marked
*illustrative* where it appears. **Correct any of them and the relevant exhibit should be redrawn.**

| Assumption | Value used | Where it appears |
|---|---|---|
| Operator revenue per unit per month | €700 | Residual Radar, Five Moves |
| Average vehicle acquisition cost | €22,000 | Residual Radar |
| Average disposal value at 24 months | €14,000 | Residual Radar |
| Operator net margin | 4% *(this one is yours, from the review)* | Throughout |
| Ancillary share of revenue | 25–35% | Five Moves |
| Ancillary contribution margin | 80–90% | Five Moves |
| Fully loaded salesperson cost | €90,000 | Agentic GTM, Five Moves |
| Cost to serve, human onboarding | €13,000 / account / year | Five Moves |
| Cost to serve, agent onboarding | €1,500 / account / year | Five Moves |
| WeYield cost base split | ~€1.4M total, ~5 of 9 heads in engineering | Strategy document |
| Model inference cost per brief | €0.12–0.20 | Monday Brief spec |

---

## Anything else

Wrong, missing, or worth arguing about — put it here, or open an issue.

| From | Note | |
|---|---|---|
| | | |
