# Learning Plan — v004

- **Written:** 2026-09-07 (AEST)
- **Owner:** Curriculum (reports to Mentor)
- **Prior:** v003
- **Status:** active — three P0 cycle only; rebuilt IDs; Lucas evidence (ranges floored); one Analyst run (`20260906T231515Z`)

## Rationale

v003 was structurally sound and not executable: fourteen active targets across ~43 weekdays, several needing 3–4 point moves, while `prod-ship` alone is multi-week. v004 cuts to **three P0 competencies** for the 60-day window.

**The three:** `prod-ship`, `api-auth`, `cust-discovery`.

**Why this combination for an FDE hiring manager.** The strongest visible evidence in 60 days is a portfolio a manager can poke and read: (1) a live system you shipped and kept under real use — the hard gate, without which FDE claims do not land; (2) a production-grade API + auth integration into that system — the customer-system wiring FDEs are hired to do, and Analyst-flagged this run; (3) a discovery script plus one worked example — proof you can surface the real problem behind the stated one, also Analyst-flagged, and the artifact is buildable in days rather than quarters. Weight went to **buildable-and-shippable** over broadly useful: these three produce a running system, an integration, and a customer-facing write-up. That is the FDE job in miniature.

**What this cycle gives up (visible in "Not this cycle", not deleted):**
- `ambiguity-decomp` — the signature interview round; sacrificed so the cycle ships integration + discovery artifacts instead of interview-theater plans. Biggest interview risk.
- `exec-comm` — largest evidence gap (1→5) but hard to ship as visible product evidence in 60 days; practice folds into discovery write-ups informally, not as a P0.
- `prod-ownership` — partially absorbed into the `prod-ship` multi-week arc (own one failure cycle on the live system) rather than a separate P0.
- `legacy-data` — Analyst-flagged; deferred so `api-auth` can land on the live substrate first.
- `llm-integrate` / `eval-design` / `context-eng` / `agent-orch` — Applied AI depth waits until production substrate and auth path exist.
- `prod-lang`, `codebase-debug`, `scope-write`, `enterprise-auth`, `cloud-deploy`, `compliance-deploy` — real gaps, not this cycle's visible-evidence bet.

Numbers: where Lucas gave a range, the **lower** figure is used and marked provisional until he confirms.

## Operating rules

1. Hold a **30% study / 70% build** split **inside these three** — not across the full matrix.
2. Never edit a written plan version. Always add a new numbered version with a diff against the prior version and a one-paragraph rationale.
3. Canonical latest: `/workspace/context/plan.md`. Snapshots: `/workspace/context/plan/vNNN.md` (+ `.diff`).
4. Mentor picks **one** daily target from the three P0s (or the study slice of the active week). Curriculum does not set the day-of pick.
5. Each new version goes to Mentor and Herald.
6. Evidence and targets are Lucas-only — never invent or overwrite scores when rewriting.

## Score convention (this version)

| id | evidence | target | notes |
|----|----------|--------|-------|
| prod-ship | 2 | 4 | target floored from `4-5` — provisional until Lucas confirms |
| api-auth | 2 | 5 | as written |
| cust-discovery | 1 | 4 | as written |

## Active targets — this cycle (three P0s)

### Build — 70% of cycle effort

| id | evidence→target | build artifact | rough size |
|----|-----------------|----------------|------------|
| prod-ship | 2 → 4 | Ship one small system and keep it running under real use (debug + iterate, not a disposable demo). Include at least one owned failure cycle (absorbs the deferred `prod-ownership` intent). | ~18–20 weekdays (~4 weeks) |
| api-auth | 2 → 5 | Integrate a real API with production-grade auth into or alongside that live system (not a toy curl script). | ~8–10 weekdays (~2 weeks) |
| cust-discovery | 1 → 4 | Structured discovery script + one worked example that surfaces the real problem behind the stated one. | ~6–8 weekdays (~1.5–2 weeks), after a short study slice |

### Study — 30% of cycle effort

Study is not a fourth competency. It is time **inside** the three:

| when | tied to | study focus |
|------|---------|-------------|
| Week 1 (front of prod-ship) | prod-ship | How production systems are operated and debugged under real usage — enough to avoid building a demo |
| Start of api-auth week | api-auth | Production auth patterns (token/session/OIDC basics) before wiring |
| Start of cust-discovery week | cust-discovery | Discovery methods that separate symptom from constraint — then immediately build the script + worked example |

Rough split across 8 weeks: ~2.5 weeks study-shaped, ~5.5 weeks build-shaped (30/70).

## 8-week sequence

| weeks | focus | days (approx) | lane |
|-------|-------|---------------|------|
| **1–4** | `prod-ship` — stand up the live system, keep it running, take it through one failure cycle | ~18–20 weekdays | mostly build; week 1 opens with a short study slice |
| **5–6** | `api-auth` — production-grade API + auth on/alongside that system | ~8–10 weekdays | short study open, then build |
| **7–8** | `cust-discovery` — methods study, then script + one worked example | ~8–10 weekdays | ~30% study / 70% build inside these two weeks |

Mentor still picks one daily target; the table is the week boundary, not a substitute for `today.md`.

## Analyst flags in play (one run only)

| id | demand | evidence | persistent across 2 runs? | this cycle? |
|----|--------|----------|---------------------------|-------------|
| api-auth | 4 | 2 | no — first run | **yes — P0** |
| cust-discovery | 4 | 1 | no — first run | **yes — P0** |
| ambiguity-decomp | 4 | 2 | no — first run | not this cycle |
| exec-comm | 4 | 1 | no — first run | not this cycle |
| legacy-data | 4 | 1 | no — first run | not this cycle |

Rewrite on persistence still waits for a second confirming Analyst run.

## Not this cycle

Visible on purpose. Still real gaps. Not deleted.

| id | evidence→target (floored) | why deferred |
|----|---------------------------|--------------|
| ambiguity-decomp | 2 → 4 | Signature interview gate; deferred so this cycle ships system + auth + discovery artifacts |
| exec-comm | 1 → 5 | Largest soft gap; weak as standalone shipped evidence in 60 days |
| prod-ownership | 1 → 5 | Intent folded into `prod-ship` failure-cycle requirement |
| legacy-data | 1 → 4 | Analyst-flagged; waits until auth path exists on the live system |
| llm-integrate | 2 → 5 | evidence floored from `2-3`; needs live substrate first |
| eval-design | 2 → 5 | Pairs with LLM path — later |
| context-eng | 3 → 5 | Already strongest Applied AI score — later deepening |
| agent-orch | 3 → 5 | target carried as Lucas wrote (`5*`); later |
| scope-write | 2 → 5 | Natural follow-on after discovery lands — next cycle candidate |
| prod-lang | 1 → 4 | evidence floored from `1-2`, target floored from `4-5`; standing depth, not this cycle's visible bet |
| codebase-debug | 1 → 4 | Critical long-term; practice opportunistically inside `prod-ship`, not a P0 |
| enterprise-auth | 2 → 4 | Adjacent to `api-auth`; deepen after the first auth integration ships |
| cloud-deploy | 2 → 4 | evidence floored from `2-3`, target floored from `4-5`; use if `prod-ship` needs it, not a P0 |
| compliance-deploy | 3 → 5 | Strength lane — apply when a customer-shaped constraint appears |

## Diff vs v003

- Collapsed fourteen active targets to three P0s (`prod-ship`, `api-auth`, `cust-discovery`)
- Moved all other competencies to an explicit "Not this cycle" section
- Replaced suggested-order list with an 8-week boundary table and day counts
- Forced single-number evidence/target (floor ranges; mark provisional)
- Applied 30/70 inside the three only
- Kept single-Analyst-run caveat and two-run persistence rule unchanged
