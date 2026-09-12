# WeYield Monday Brief
## Product specification — an AI-native service the current team can ship in eight weeks

**Working name:** Monday Brief (fits the house naming — Market Radar, Performance Hub, Revenue Horizon, Pricing Insights). Emmanuel names it.
**Prepared by:** Ram Badrinathan · September 2026 · v0.1 for discussion
**Depends on:** *WeYield — Building the AI-Native Business* (strategy) — this spec is Horizon 1 items b, c, d and e delivered as one product.

---

# 0. One page

**What it is.** Every Monday, every WeYield account receives a short, data-grounded brief written in the voice of a WeYield coach: what moved last week across their stations, what the market did, what is coming, and the three things their revenue manager should do this week — each with a euro value and a "what happens if you do nothing". The reader replies **DONE**, **SKIP** or **WHY 2**; a WHY gets an answer in the thread, grounded in the same figures.

**Who reads it.** The owner or general manager — the persona WeYield's site already lists ("CEO & Managing Director — strategy and financial performance") and currently has nothing for. Also the revenue manager, and the RM consultants who run WeYield across several operators.

**Why this product first.** It uses only data WeYield already holds. It needs no partnership, no new integration and no user interface. It productises the coach — the encoded methodology is the corpus everything later depends on. It puts a WeYield artefact in the owner's inbox every week. It instruments the accept / reject loop that the Decision Feed and outcome pricing will need. And a two-person pod can ship it in eight weeks — which is the existence proof for the cost thesis.

**What it is not.** It does not write rates. It does not forecast — it uses Revenue Horizon's forecasts. It does not touch fleet value or residuals (that needs the Indicata partnership — Horizon 2). It invents no numbers: every figure in every sentence is traceable to a computed fact, enforced by a verifier, or the sentence is dropped.

**What it costs to run.** Roughly **€0.15–0.30 per brief** at frontier-model list prices — under **€2,000 a year** for the whole base at weekly cadence. Olivier's review flagged token cost as a new cost line; for this product it is about 0.1% of revenue. The cost that matters is the coach hour it replaces.

**How it is sold.** Included in the Pricing Insights tier as a retention and ACV lever; a per-station or per-vehicle add-on for Performance-Hub-only accounts; per managed operator for consultants. Four free briefs, then paid. Positioned as *"your revenue coach, every Monday"* — never as AI.

**Team.** Two engineers from the existing five, one coach at 30%, Emmanuel at 10%. Nobody hired. The old stack stays frozen.

---

# 1. Why this product, not the others

The strategy document lists five candidate first builds. Scored against what the *immediate* team can do:

| Candidate | Uses only held data | No partnership needed | 2 people, ≤8 weeks | Sellable on its own | Reaches the owner | Creates the telemetry loop | Encodes the methodology |
|---|---|---|---|---|---|---|---|
| Conversational Analyst (ask-your-data) | Yes | Yes | Yes | Weak — a feature | No | Partly | No |
| **Monday Brief** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** | **Yes** |
| Answer-layer monitoring | Yes (scraping) | Yes | Borderline — fragile targets | Yes | Partly | No | No |
| Decision Feed (daily, guardrailed) | Yes | Yes | No — needs methodology + telemetry first | Yes | Partly | Yes | Requires it |
| Fleet P&L | No — residual data | **No** | No | Yes | Yes | Yes | No |

The Brief is the only candidate that clears every column. It also *contains* the Analyst — the reply channel is the Analyst with a narrower, safer surface — and it is the Decision Feed at weekly cadence with a human in the loop. Nothing built here is thrown away.

---

# 2. Users and the job to be done

## 2.1 Three readers

| Reader | Today | With the Brief | Why they pay |
|---|---|---|---|
| **Owner / GM / CEO** of a franchisee or independent (50–3,000 cars) | Sees a dashboard rarely; hears about revenue when the RM raises it; decides fleet and pricing questions by gut in a weekly meeting | Five minutes on Monday morning, in their language, on their phone. Knows what moved, what the market did, and what is being done about it | Control without a dashboard. The three actions carry euro values — this is the first WeYield artefact that speaks P&L |
| **Revenue manager** (WeYield's current user) | Opens Performance Hub and Market Radar daily; writes their own weekly summary for the boss; reacts to competitor alerts one by one | Receives the same brief as the owner — so the conversation with the boss starts from shared facts — plus the action list as their agenda | Saves the weekly write-up. Gives them the coach's judgement on demand |
| **RM consultant** running WeYield for several operators | Writes a weekly note per client by hand, from the same screens, 45–60 minutes each | One brief per client, drafted; edits for five minutes and forwards under their own name | Serves twice the clients with the same hours. This is the consultant channel as a multiplier |

**Internal reader (free, week 6):** WeYield's own sales and coaching team receives an *internal edition* per account — the same facts with a churn-risk lens: utilisation falling, alerts ignored for three weeks, no logins. Account management on autopilot.

## 2.2 The job

> "Tell me in five minutes, every Monday, what happened across my stations last week, what is coming, and what my revenue manager should do — in my language, without opening a dashboard."

## 2.3 What replaces what

The coach's weekly note for top accounts (assumed 45–60 minutes each, today done for a minority of accounts) becomes a five-minute edit. For the ~100 accounts that get no coach note today, the Brief is new value at near-zero marginal cost. That is the whole cost-to-serve argument in one product.

---

# 3. The product

## 3.1 Anatomy of a Brief

400–600 words. Seven blocks, always in this order. Blocks with nothing to say are omitted, not padded.

| # | Block | Content | Source of truth |
|---|---|---|---|
| 1 | **Headline** | One sentence: the single most important thing this week | Composer, from the top-ranked candidate action |
| 2 | **Last week in numbers** | RPD, utilisation, bookings taken, pace — vs last year and vs forecast; top mover up, top mover down, by station × car group | Performance Hub (deterministic table, not prose) |
| 3 | **Market** | Competitor rate moves: who cut, who held, where, by how much. Cross-tenant benchmark for opted-in accounts ("comparable operators in your markets are X% above you for October") | Market Radar; benchmark aggregates with k ≥ 5 |
| 4 | **Ahead** | Demand signal for the next 4–8 weeks — inbound seat capacity, search trend; on-the-books pace for the upcoming windows vs last year | Revenue Horizon; Performance Hub |
| 5 | **This week's three actions** | Ranked. Each: what · where · why (with figures) · estimated € value · what happens if you do nothing · confidence | Rules engine (candidates and values) + Composer (ranking and explanation) |
| 6 | **Watch items** | Anomalies and data gaps — utilisation below the account's own floor, feeds missing days, alerts unresolved | Facts builder |
| 7 | **Reply line** | "Reply DONE 1 · SKIP 2 · WHY 3 — or ask anything" | Reply handler |

**Sources line** at the foot: Performance Hub week reference, Market Radar alert IDs, Revenue Horizon forecast run — every figure is one click from its origin.

## 3.2 Cadence, channels, languages

- **Cadence:** weekly, Monday 06:30 local to the account's head office. Daily cadence for top accounts is a Horizon 2 option once telemetry proves the weekly one.
- **Channels:** email (default); WhatsApp Business for markets where that is how owners read (islands, North Africa — verify by region); PDF attached for forwarding. In-app later, not v1.
- **Languages:** the facts pack is language-neutral; the Composer writes in the account's language. French, English, Spanish, Italian, German, Portuguese from day one; others on request. This matters disproportionately across 50 countries and costs nothing extra.
- **Recipients:** configured per account — owner, RM, consultant. Same brief to all; the RM's copy carries the action list as a checklist.

## 3.3 The reply loop — the Analyst, narrowed

- **DONE n / SKIP n / MODIFIED n [text]** → recorded as telemetry against the action. A one-line acknowledgement.
- **WHY n** → the Analyst answers in the thread within two minutes, grounded in the same facts pack, allowed to run a bounded set of drill templates (by station, car group, window, channel — parameterised queries, never free SQL). Every figure in the answer is verified the same way as the brief.
- **Any other question** → Analyst mode over the facts pack and the drill templates. If the question needs data outside the pack ("what did we do in 2023?"), it says so and offers to route to the coach.
- **No action is a valid brief.** If no rule fires, block 5 reads: *"No action recommended this week — pace and rates are where they should be."* The product must be allowed to say nothing. Manufacturing actions to look useful is the failure mode.

## 3.4 The coach in the loop

Accounts are tiered by ACV.

- **Tier A (top ~20):** the brief is created as a **draft in the coach's own mailbox**. The coach edits — usually a sentence or two — and sends under their name. Five minutes. No review interface to build.
- **Tier B/C (the rest):** auto-sent from `brief@weyield.io`, signed "Your WeYield coaching team". A daily digest to the coaching lead lists what went out and any verifier warnings.
- Anything the verifier flags (see §5) is held and routed to a coach regardless of tier.

The coach's edits are captured as training signal: what they changed, and why, becomes next quarter's rule refinements and style exemplars.

---

# 4. A sample Brief

*Illustrative — fictional operator, stations and figures. Demonstrates format, voice and the reasoning contract only.*

---

**Riviera Cars · Monday Brief · Week 36 (31 Aug – 6 Sep 2026)**
*For: Sophie Marchetti (GM) · Karim Belaïd (Revenue Manager)*

**Hold your compact rates at Nice Airport for the October half-term — pace is nine points ahead of last year even though two competitors cut on Tuesday — and move twelve idle intermediates from Toulon before the 18th.**

**Last week in numbers**

| | This week | vs LY | vs forecast |
|---|---|---|---|
| RPD | €68.40 | +3.1% | +1.8% |
| Utilisation | 79% | −2 pts | −1 pt |
| Bookings taken | 1,284 | +6% | +4% |
| Top mover ↑ | NCE Airport · Compact RPD | +7% | |
| Top mover ↓ | Toulon · Utilisation | 61% | third week below your 70% floor |

**Market.** Competitor A cut Compact (ECMR) at Nice Airport by 6% on Tuesday [MR-4471]; Competitor B held. On the broker channel you are 4th on price for Intermediate (CDMR) at Nice for 12–19 October [MR-4480]. Comparable Mediterranean airport franchisees (7 operators, anonymised) are running October compact rates 4% above yours [BM-oct-ecmr].

**Ahead.** Inbound seat capacity to Nice for 12–25 October is +5% on last year (UK +9%, Germany +3%) [RH-0906]. Search interest for Nice car hire in October is up 11% week on week [RH-0906-s]. For 12–19 October you already hold 91% of last year's final compact bookings and 72% of intermediates [PH-pace-w41].

**This week's three actions**

**1 · Hold Compact rates at Nice Airport for 12–19 October. Do not follow Competitor A's cut.**
You are nine points ahead of last year's pace at this date and 91% of the way to last year's final volume [PH-pace-w41]. Following the cut would give away an estimated **€4,100** across the remaining bookings. If you do nothing different: you very likely sell out anyway. *Confidence: high.*

**2 · Move 12 Intermediates from Toulon to Nice Airport by 18 October.**
Toulon has 14 CDMR idle for five days or more [PH-fleet-TLN]; Nice Airport shows a forecast shortfall of 11 CDMR for 18–20 October [PH-fc-NCE]. Transfer cost about €47 a unit; net upside about **€2,100**. If you do nothing: Nice turns away intermediate demand while Toulon pays to park them. *Confidence: medium — depends on Toulon's own October pickup.*

**3 · Open an upgrade step Compact → Intermediate at Marseille Airport, October weekends, +€9 a day.**
Compact is forecast to sell out both October weekends at Marseille; Intermediate sits at 68% [PH-fc-MRS]. Estimated **€1,300**. *Confidence: medium.*

**Watch.** Toulon utilisation 61% — third consecutive week below your 70% floor; worth a conversation about October fleet size there. Monaco data feed missed 2–3 September [DQ-MCO]; Monaco figures above exclude those two days.

Reply **DONE 1**, **SKIP 2**, **WHY 3** — or ask anything.

*Sources: Performance Hub W36 · Market Radar alerts 4471, 4480 · Revenue Horizon run 6 Sep · Benchmark cell oct-ecmr (n=7). Your WeYield coaching team.*

---

Three things to notice in the sample. Every number carries a reference. The value estimates state their method implicitly through the evidence. And the Toulon watch item is the *owner's* decision — fleet size — surfaced by revenue data. That is the first step up the value chain, taken with data WeYield already holds.

---

# 5. The reasoning contract and guardrails

These are product rules, not engineering preferences. They are what make the Brief sellable to an industry whose stated adoption blocker is black-box distrust.

1. **The model never computes.** Every number in prose comes from the facts pack, which is built deterministically. The Composer receives values and writes sentences around them. It is forbidden, in the prompt and by the verifier, to add, subtract, percentage or estimate.
2. **Every claim carries a reference.** Each sentence in the structured output carries `refs: []` pointing at fact IDs. A sentence with a number and no reference is dropped before send.
3. **Actions come from rules, not from the model.** The rules engine generates candidate actions with evidence and value estimates. The Composer ranks, selects up to three, and explains. It cannot originate an action the rules did not propose. New actions are added by adding rules — with the coach — not by prompting.
4. **The Brief recommends; the human executes.** v1 writes no rates and moves no cars. Pricing Insights write-back remains the execution path, triggered by a person.
5. **Competitor information is what the customer already sees** in Market Radar — nothing more.
6. **Benchmarks are opt-in and k-anonymous.** A cell is shown only if the account has opted into the benchmark exchange and the peer set has at least five operators. Cells are indices, never absolute rates.
7. **Confidence is stated, and hedged where the forecast is the basis.**
8. **Missing data renders as missing.** Never as zero. The Monaco line in the sample is the pattern.
9. **A quiet week is a valid brief.** Zero actions is an allowed and expected output.
10. **The verifier is a hard gate.** Numeric fidelity below 100% holds the brief for a coach. There is no "mostly right" send.

---

# 6. Architecture

## 6.1 Pipeline

```
Performance Hub / Market Radar / Revenue Horizon data
        │
        ▼
[1] Facts Builder            deterministic SQL/Python · per account per week
        │                    → facts.json (KPIs, movers, pace, competitors, forecast, fleet, benchmark, data quality)
        ▼
[2] Rules Engine             methodology encoded as rules · each fires with evidence + value estimate
        │                    → candidates.json
        ▼
[3] Composer (LLM)           coach persona + style guide + reasoning contract (cached prefix)
        │                    + facts + candidates + account profile + last 4 briefs + telemetry summary
        │                    → brief.json (blocks, sentences, refs, language)   [structured output]
        ▼
[4] Verifier                 (a) deterministic: every numeric token ↔ a fact value; every sentence has refs or is connective
        │                    (b) LLM judge on a sample: action logic, tone, brevity rubric
        │                    fail → drop sentence / regenerate once / hold for coach
        ▼
[5] Renderer                 email HTML · WhatsApp text · PDF · coach draft
        ▼
[6] Delivery                 tier A → draft in coach mailbox · tier B/C → auto-send · digest to coaching lead
        ▼
[7] Reply Handler            DONE / SKIP / MODIFIED → telemetry · WHY / free text → Analyst over facts + drill templates
        ▼
[8] Telemetry                briefs · actions · responses · outcomes at T+7 and T+28 on the action's scope
```

Nothing in [1], [2], [4a], [5], [6] or [8] involves a model. The model does two things: write, and answer. That is the correct shape — deterministic core, generative surface — and it is the same shape the Decision Feed will have.

## 6.2 Facts pack — schema skeleton

Every fact has a stable `id`, a `source` (PH, MR, RH, BM, DQ) and a `link`. Values are typed and unit-bearing. This is the only thing the Composer is allowed to quote.

```json
{
  "account": {
    "id": "acc_riviera", "name": "Riviera Cars", "type": "franchisee",
    "language": "fr", "currency": "EUR", "tier": "A",
    "stations": ["NCE-AP", "NCE-CTY", "CEQ", "MRS-AP", "TLN", "MCO"],
    "car_groups": ["MCMR", "ECMR", "CDMR", "IDAR", "SFAR"],
    "prefs": { "util_floor": 0.70, "benchmark_opt_in": true, "channels": ["email"] },
    "recipients": [{ "role": "gm", "name": "…", "email": "…" }, { "role": "rm", "…": "…" }]
  },
  "period": { "iso_week": "2026-W36", "from": "2026-08-31", "to": "2026-09-06", "generated_at": "2026-09-07T04:30:00Z" },
  "kpis": [
    { "id": "PH-rpd-w36", "metric": "rpd", "scope": { "station": "*", "group": "*" },
      "value": 68.40, "unit": "EUR", "vs_ly": 0.031, "vs_forecast": 0.018, "source": "PH", "link": "https://…" }
  ],
  "movers": [
    { "id": "PH-mv-1", "metric": "rpd", "scope": { "station": "NCE-AP", "group": "ECMR" }, "delta_vs_ly": 0.07, "direction": "up", "source": "PH", "link": "…" }
  ],
  "pace": [
    { "id": "PH-pace-w41", "window": { "from": "2026-10-12", "to": "2026-10-19" }, "scope": { "station": "NCE-AP", "group": "ECMR" },
      "otb_vs_ly_final": 0.91, "pace_pts_vs_ly": 9, "source": "PH", "link": "…" }
  ],
  "competitors": [
    { "id": "MR-4471", "competitor": "A", "scope": { "station": "NCE-AP", "group": "ECMR" }, "change": -0.06, "observed": "2026-09-01", "source": "MR", "link": "…" }
  ],
  "forecast": [
    { "id": "RH-0906", "signal": "seat_capacity", "market": "NCE", "window": { "from": "2026-10-12", "to": "2026-10-25" },
      "delta_vs_ly": 0.05, "breakdown": { "UK": 0.09, "DE": 0.03 }, "source": "RH", "link": "…" }
  ],
  "fleet": [
    { "id": "PH-fleet-TLN", "scope": { "station": "TLN", "group": "CDMR" }, "idle_units": 14, "idle_days_min": 5, "source": "PH", "link": "…" },
    { "id": "PH-fc-NCE", "scope": { "station": "NCE-AP", "group": "CDMR" }, "window": { "from": "2026-10-18", "to": "2026-10-20" }, "shortfall_units": 11, "source": "PH", "link": "…" }
  ],
  "benchmark": {
    "opted_in": true,
    "cells": [{ "id": "BM-oct-ecmr", "peer_set": "med_airport_franchisee", "n": 7, "metric": "rate_index_oct_ecmr", "value": 1.04, "source": "BM" }]
  },
  "data_quality": [{ "id": "DQ-MCO", "station": "MCO", "missing_days": ["2026-09-02", "2026-09-03"] }]
}
```

## 6.3 Rules engine — v0 rule set

Ten rules to start. Each rule declares its trigger, its evidence facts, its value method and a confidence policy. The coach owns this list; engineering owns the runtime. Target: 25–30 rules by week 8, one added or refined per week thereafter from coach edits and telemetry.

| # | Rule | Trigger (over facts) | Candidate action | Value method | Confidence |
|---|---|---|---|---|---|
| R1 | **Pace-ahead hold** | `pace_pts_vs_ly ≥ +5` and `otb_vs_ly_final ≥ 0.85` for a window ≥ 3 weeks out, and a competitor cut in the same scope within 7 days | Hold (or test +x%) — do not follow the cut | expected remaining rentals × (current rate − competitor rate) | High if both conditions strong; medium otherwise |
| R2 | **Pace-behind, undercut** | `pace_pts_vs_ly ≤ −5` and ≥ 2 competitors cut ≥ 5% in scope within 7 days | Targeted cut on the affected channel only | expected incremental rentals × rate − dilution on existing bookings | Medium |
| R3 | **Idle vs shortfall transfer** | station A `idle_units ≥ 8` for `≥ 5 days` in group G; station B forecast `shortfall_units ≥ 5` in G within 21 days | Move n units A → B before date | expected revenue at B − transfer cost × n | Medium; high if B is the account's main airport |
| R4 | **Upgrade ladder** | group G forecast sold out on ≥ 2 dates in window; G+1 utilisation forecast ≤ 75% same dates | Open upgrade step G → G+1 at +€x/day | sold-out days × expected upgrades × €x | Medium |
| R5 | **Utilisation floor** | station utilisation below the account's `util_floor` for ≥ 3 consecutive weeks | Watch item; if forecast persists → suggest fleet-size conversation | none (watch) | — |
| R6 | **Market growing, you are not** | Revenue Horizon demand `delta_vs_ly ≥ +5%` for market M and pace `≤ 0` in M | Investigate rate positioning / channel visibility in M | (informational — quantified as pace gap × ADR) | Medium |
| R7 | **Alert backlog** | ≥ 5 Market Radar alerts unresolved for the same scope over 14 days | Consolidate: one positioning decision for the scope | none | — |
| R8 | **Length-of-rent drift** | share of 1–2 day rentals up ≥ 5 pts vs LY at an airport station | Review minimum-LOR rules for peak dates | dilution estimate | Low–medium |
| R9 | **Event window check** | known event / holiday in next 6 weeks in market M (calendar fact) and pace flat | Pre-position rates for the window | pace gap × ADR | Medium |
| R10 | **Data integrity** | any `data_quality` entry | Watch item, with the affected figures footnoted | none | — |
| R0 | **Quiet week** | no R1–R9 fired | *"No action recommended this week"* | — | — |

Rules never touch the model. Their output is the *only* pool the Composer may draw actions from.

## 6.4 Composer — prompt contract

The system prompt is frozen and cached. Volatile inputs arrive after it.

**System prompt sections (stable, cached):**
1. *Persona* — a WeYield coach: direct, specific, respectful of the operator's judgement, writes for a busy owner. Never says "AI". Never uses filler.
2. *Style guide* — 20 exemplar sentences and 3 exemplar briefs from real coach notes (anonymised), plus a banned-phrases list.
3. *Reasoning contract* — the ten rules in §5, phrased as instructions: quote only facts; attach refs; select actions only from candidates; never compute; zero actions is valid; state confidence.
4. *Output schema* — the brief JSON (enforced via structured output, not prose instruction).
5. *Language policy* — write in `account.language`; keep station codes and product names as-is; localise dates and currency.

**Volatile inputs (after the cache breakpoint):**
- `facts.json` · `candidates.json` · account profile · the last four briefs (headlines and actions only, so the voice stays consistent and it does not repeat itself) · telemetry summary (which past actions were done/skipped — so it stops recommending what the account always skips, and says so once).

**Output schema (structured):**

```json
{
  "language": "fr",
  "headline": { "text": "…", "refs": ["PH-pace-w41", "MR-4471", "PH-fleet-TLN"] },
  "numbers_table": "rendered deterministically from facts — not generated",
  "market": [{ "text": "…", "refs": ["MR-4471"] }],
  "ahead": [{ "text": "…", "refs": ["RH-0906", "PH-pace-w41"] }],
  "actions": [
    { "candidate_id": "act_1", "rank": 1, "title": "…", "why": { "text": "…", "refs": ["…"] },
      "value_eur": 4100, "if_nothing": "…", "confidence": "high" }
  ],
  "watch": [{ "text": "…", "refs": ["PH-kpi-TLN-util", "DQ-MCO"] }],
  "omitted_blocks": ["benchmark"],
  "composer_notes": "internal — anything the model wants a coach to know"
}
```

Note that `numbers_table` is *not* generated — it is rendered from facts by the renderer. The model writes prose; the deterministic layer writes numbers wherever it can.

## 6.5 Verifier

**Deterministic pass (every brief, hard gate):**
- Extract every numeric token from every generated sentence (currencies, percentages, points, counts, dates).
- Match each against a fact value in the referenced `refs` — with formatting tolerance (68.4 / €68.40 / 68,40 €) but no arithmetic tolerance.
- Every sentence containing a number must carry ≥ 1 ref whose values account for all its numbers.
- Every `candidate_id` in actions must exist in `candidates.json`; `value_eur` must equal the candidate's value.
- Failure handling: drop the offending sentence and re-verify; if the headline or an action fails, regenerate once with the failure as feedback; if it fails again, hold for coach.

**LLM-judge pass (sample of 10% weekly, plus every held brief):**
- Rubric 1–5 on: does each action follow from its evidence; is the tone the coach's; is anything redundant; would an owner act on this.
- Scores feed the weekly rule/prompt review with the coach. Nothing ships or is blocked on the judge alone.

## 6.6 Reply handler and the Analyst

- Inbound email via a transactional-mail inbound webhook (or WhatsApp Business webhook). Thread matched to `brief_id` by header token.
- `DONE|SKIP|MODIFIED n [text]` parsed deterministically → `action_responses`.
- Anything else → Analyst call: same persona and contract, input = facts pack + the brief + the question; tools = 6–10 **drill templates** (parameterised queries: KPI by station × group × window × channel; pace curve for a window; competitor history for a scope; forecast detail for a market). No free-form SQL. Answer verified the same way. Reply in-thread.
- Out-of-scope questions get an honest *"that is outside this week's pack — I'll flag it to your coach"* and a ticket to the coaching lead.

## 6.7 Telemetry schema

```
briefs           id · account_id · iso_week · language · tier · channel · sent_at · opened_at
                 composer_model · tokens_in · tokens_cached · tokens_out · cost_eur · verifier_result · coach_edited (bool) · edit_diff
brief_actions    id · brief_id · candidate_id · rule_id · rank · scope · value_eur_est · confidence · if_nothing
action_responses action_id · response (done|skip|modified) · text · responded_at · via (email|wa|app)
outcomes         action_id · horizon (t+7|t+28) · metric (rpd|util|bookings) · scope · actual · baseline (forecast at brief time) · delta
analyst_turns    brief_id · question · answer · refs · templates_used · verified · latency_ms · cost_eur
```

`outcomes` is the point of the whole thing. In six months it answers: which rules make money, for which kind of account, at what confidence — and it is the evidence base for outcome pricing and for the Decision Feed's learning loop. It cannot be backfilled.

---

# 7. Model, cost and data residency

## 7.1 Model

- **Composer and Analyst:** a frontier model — the Brief's quality *is* the writing and the judgement in selecting and explaining actions across six languages. Current recommendation: Claude Opus 5 (`claude-opus-5`), adaptive thinking at medium effort, structured output for the brief schema, prompt caching on the frozen system prompt.
- **Verifier (a):** no model — deterministic.
- **Verifier (b) judge:** the same model on a 10% sample. A smaller model is acceptable here if cost ever matters; it will not.
- **Generation mode:** weekly briefs are not latency-sensitive → use the **Batch API** (asynchronous, 50% of list price). Analyst replies are interactive → standard API, streamed.

## 7.2 Cost per brief — worked

Assumptions: frozen system prompt ~10K tokens (cached); volatile input ~8K; output ~2K brief plus ~3K thinking; verifier judge on 10%; 30% of briefs receive one Analyst question (~12K in, ~2K out).

| Component | Tokens | List price (Opus 5) | Cost |
|---|---|---|---|
| Composer — cached prefix | 10K read | $0.50 / M | $0.005 |
| Composer — volatile input | 8K | $5 / M | $0.040 |
| Composer — output incl. thinking | 5K | $25 / M | $0.125 |
| Verifier judge (10% sample, amortised) | ~1K in / 0.2K out equiv. | | $0.010 |
| Analyst reply (30% of briefs, amortised) | 3.6K in / 0.6K out equiv. | | $0.033 |
| **Per brief, standard API** | | | **≈ $0.21 (≈ €0.19)** |
| **Per brief, Composer via Batch API (−50%)** | | | **≈ $0.13 (≈ €0.12)** |

**Annual, whole base, weekly:** 120 accounts × 52 ≈ 6,240 briefs → **$800–1,300 a year**. At five times the volume (daily for top accounts, internal edition, consultants' clients) still under **$7,000**. Set the budget line at €5,000 and stop discussing it. The relevant cost is the coach hour, not the token.

## 7.3 Data residency and privacy

- The facts pack contains **no traveller personal data** — aggregates, rates, counts, forecasts. Recipient names and emails are held in WeYield's systems and merged at render time, not sent to the model. This keeps the LLM processor outside the personal-data path for GDPR purposes, though it is still a sub-processor for business-confidential data and must be listed as such in the DPA.
- **EU inference:** run the model through an EU region — Claude on Amazon Bedrock (EU regions) or Vertex AI (`eu`), or the first-party API's inference-geography controls where available. Confirm zero-data-retention terms with the provider in week 1; it is a standard enterprise ask.
- Cross-tenant benchmark aggregates: k ≥ 5, index form only, opt-in — and reviewed once by counsel against existing customer terms before the block is switched on (open question 5).

---

# 8. Packaging and pricing

**Positioning:** *"Your revenue coach, every Monday."* Owners buy RPD, utilisation and hours back — not model names. The word "AI" appears in the sub-processor list and nowhere else.

**Three packaging tests, run in parallel across the pilot cohort (weeks 5–8):**

| Package | Who | Price hypothesis | What it tests |
|---|---|---|---|
| **A · Included** | Pricing Insights tier accounts | Included; measured as retention and upsell lift | Does the Brief move renewals and pull Performance-Hub-only accounts up a tier |
| **B · Add-on, per vehicle** | Performance Hub–only accounts | $1.00–1.50 per vehicle per month (300 cars → ~€3.5–5K a year) | Willingness to pay for coach judgement without buying the pricing engine |
| **C · Consultant** | RM consultants | €150–250 per managed operator per month | The channel economics |

Anchor for B: it costs less than one hour of a coach per week, and the first pilot briefs will carry three quantified actions per week — the value is on the page. **Trial:** four free briefs, then paid. If B converts above 30% of Performance-Hub-only accounts in the pilot, it becomes the lever that lifts blended ACV from €12.5K toward €16K in Year 1 — the number the strategy document assumed.

---

# 9. Build plan — eight weeks

**Team.** Engineer 1 (data/backend): facts builder, rules runtime, delivery, telemetry, reply parsing. Engineer 2 (AI): composer, structured output, verifier, evals, Analyst, drill templates. Coach (30%): methodology → rules, style guide and exemplars, tier-A review, weekly rule review. Emmanuel (10%): design-partner recruitment and calls, pricing decision. One salesperson (10%, weeks 5–8): pricing tests. Everyone else: maintenance on the frozen stack.

| Week | Deliverable | Gate |
|---|---|---|
| **1** | Facts builder over 5 pilot accounts (mix: franchisee, independent, consultant, one WhatsApp market). Style guide from 20 anonymised coach notes. Rules R0–R5 as specification with the coach. Provider chosen; EU inference and retention terms confirmed. | Facts pack validates against schema for all 5; every fact has a link |
| **2** | Composer v0 with structured output; verifier (a); eval harness — 30 synthetic weeks replayed; numeric fidelity measured. Rules R0–R5 running. | 100% numeric fidelity on the replay set; coach rubric ≥ 3.5/5 |
| **3** | Renderer (email, PDF); coach-draft delivery; telemetry tables; reply parser (DONE/SKIP/MODIFIED). R6–R10. | First internal briefs to the coaching team on real data |
| **4** | **Pilot send** to 5 design partners, tier-A path (coach edits). Multilingual on. Analyst v0 with 6 drill templates. | Briefs land Monday 06:30 local; coach edit time ≤ 10 min; zero verifier escapes |
| **5** | Iterate on rubric and rules (target 20 rules). Benchmark block for opted-in accounts. WhatsApp channel for one market. Pricing tests A/B/C briefed to sales. | Reply rate ≥ 20% among pilots |
| **6** | Extend to 20 accounts; tier-B auto-send begins. **Internal edition** (churn lens) to sales and coaching. Batch API for weekly generation. | Cost per brief measured and ≤ €0.30; coaching lead digest live |
| **7** | 60 accounts. Outcome measurement at T+7 live. Rule review cadence set (weekly, coach + Eng 2). | ≥ 1 action DONE per account per month across pilots |
| **8** | **General availability** to the base. Pricing decision. Board readout: briefs sent, open/reply, actions accepted, coach minutes saved, cost per brief, first outcome deltas, add-on conversion. | Go/no-go on Horizon 2 sequencing |

**What this deliberately does not build:** a UI, a chatbot, a forecasting model, a rate-writing path, a fleet-value view. Each of those is a later horizon or a partnership, and each would push the eight weeks to twenty.

---

# 10. Acceptance criteria and evals

**Hard gates (product does not ship without them):**
- Numeric fidelity **100%** on the replay set and on every production brief (verifier a).
- Zero production incidents of an invented figure in the first 90 days.
- Every action traceable to a rule and a candidate ID.
- Missing data always rendered as missing; no zero substituted for unknown.

**Quality (measured, week 8 targets):**
- Coach rubric ≥ **4.0 / 5** on 30 sampled briefs (evidence → action logic; coach voice; brevity; would an owner act).
- Coach edit time on tier A ≤ **5 minutes** per brief (from an assumed 45–60 minutes to write one).
- ≥ **25%** of briefs receive a reply; ≥ **1 action DONE** per account per month.
- Open rate ≥ **60%** (email) among named recipients.

**Economics (week 8):**
- Cost per brief ≤ **€0.30** all-in.
- Add-on (package B) trial-to-paid conversion ≥ **30%** among Performance-Hub-only pilots — or a clear reason it should be bundled instead.

**Evals to build in week 2 and run on every change:**
- *Replay set:* 30 historical account-weeks with known facts → fidelity, ref coverage, action validity.
- *Adversarial set:* facts packs with gaps, contradictions, a quiet week, a data-quality flag — the brief must degrade gracefully and say nothing when there is nothing to say.
- *Language set:* the same facts pack in six languages — numbers and codes identical, prose native.
- *Regression:* any prompt or rule change reruns all three before merge.

---

# 11. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Model invents or mis-states a figure | Medium without controls; low with them | Facts-only contract; deterministic verifier as a hard gate; drop-sentence policy; hold-for-coach on any failure |
| Briefs read as generic AI text; owners stop opening | Medium | Real coach exemplars; rules-driven specificity; "no action" allowed; 400–600 words; headline first; coach voice on tier A |
| A recommended action loses money | Low–medium | v1 recommends, humans execute; confidence stated; value methods explicit; outcomes telemetry surfaces any rule that systematically misfires — retire it |
| Rules too crude for varied operators | Medium early | Start with 10 conservative rules; coach-owned weekly review; account preferences (floors, channels) in the facts pack; telemetry shows which rules get skipped where |
| Data gaps in tail accounts | High for some | Graceful degradation; data-quality block; briefs still ship with what is known |
| Coach resistance | Low–medium | Coach is editor and rule-owner, not replaced; time saved is measured and shown; tier-A drafts land in their own mailbox |
| Customer contract does not permit LLM processing or benchmark aggregation | Possible for some | Counsel review in week 1; benchmark block per-account opt-in; EU inference and no personal data in the model path |
| Performance Hub has no clean per-account query path | Unknown | Open question 1 — if true, week 1 becomes a data-access sprint and the plan slips two weeks, not eight |

---

# 12. What it unlocks

This is Horizon 1 of the strategy in a single product. Concretely:

- **Methodology encoded** (strategy item d) — the rule set *is* the written-down coaching method, and it grows weekly.
- **The loop instrumented** (item c) — `outcomes` is the evidence base for outcome pricing and for the Decision Feed's learning.
- **The Analyst shipped** (item b) — as the reply channel, with a narrower and safer surface than a chat box.
- **The owner reached** (Horizon 2's buyer change) — with data WeYield already holds; the Toulon fleet-size watch item is the first fleet conversation.
- **Cost-to-serve collapsed** — the 100 accounts that get no coach note today get one every Monday for €0.20.
- **The Decision Feed** becomes: the Brief at daily cadence, guardrails per operator, execution via Pricing Insights write-back, learning from `outcomes`. Same facts builder, same rules engine, same composer, same verifier.
- **The Fleet P&L** becomes: new fact types (acquisition cost, residual index from Indicata) and new rules (R11+: de-fleet timing). The brief already has the slot for it.

---

# 13. Open questions for Emmanuel — assumptions this spec rests on

1. **Data access.** Does Performance Hub expose a per-account API or warehouse WeYield's own engineers can query weekly, with station × car group × day grain for RPD, utilisation, bookings, pace, fleet counts and idle days? *(If not, week 1 is a data-access sprint.)*
2. **Coach notes today.** Do coaches write weekly notes for accounts now — how many accounts, in what form? *(These are the style exemplars. If none exist, the Academy material substitutes, and the first month is louder on tone review.)*
3. **Coverage.** How many accounts run all three of Market Radar, Performance Hub and Revenue Horizon? The Brief degrades gracefully without one, but the sample assumes all three.
4. **Languages.** Which six languages cover 90% of recipients?
5. **Contracts.** Do current customer terms permit an LLM sub-processor and opt-in cross-tenant aggregate benchmarking? Who reviews?
6. **Channels by region.** Where do owners read WhatsApp rather than email — islands, North Africa, Latin America?
7. **Tiering.** Confirm the top-20 accounts by ACV for the tier-A coach path — the same list the repricing exercise needs.
8. **Fleet fields.** Do idle-unit counts and station-level fleet plans already flow into Performance Hub, as the site copy implies? *(Rule R3 depends on it.)*

---

*Provenance: product facts from weyield.io (Sep 2026) and Olivier Jager's briefing of 10 Sep 2026; account, station and figure data in §4 are fictional; model prices are Anthropic list prices as of the date of writing; token budgets are engineering estimates to be replaced by measured usage in week 2.*
