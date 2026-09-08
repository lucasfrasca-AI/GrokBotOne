# Demand scoring rubric
# Owner: Mentor (absorbed from retired Analyst).
# Reconstructed 2026-09-08 from first signals.md run (`20260906T231515Z`) so later runs stay consistent.
# Source of truth for method: this file + the frozen scores in signals.md for that run.

## Scope
- Score **market demand only** (1–5) against `/workspace/context/competencies.md` IDs.
- **Never** write, infer, or overwrite Lucas’s **evidence** or **target** columns.
- After scoring, **read** evidence from competencies.md for flags only.
- Write results to `/workspace/context/signals.md`.

## Per-capture mapping
1. Read each new capture (title, snippet, URL, matched keyword).
2. Map to zero or more competency IDs where the capture shows employers/practitioners pulling that skill.
3. One capture may map to several IDs (`also` rows). Prefer the best-fit IDs; do not spray.
4. If the item is title/hiring meta with no skill content, leave **unmapped** (`—`) rather than force an ID. (First run: items 04, 05, 06, 08, 09.)

## Demand scale (1–5) — recovered from first-run notes
| Score | Meaning (as applied in run 20260906T231515Z) |
|-------|-----------------------------------------------|
| 5 | (Reserved for extreme/concentrated pull; first rebuilt-ID run did not assign 5 to any skill ID — meta hiring volume previously sat under retired `market-fit`.) |
| 4 | Explicit, direct pull for that skill: named in role work, interview gate, or concrete customer-system task matching the ID. |
| 3 | Present but secondary: called out in a role mix, implied by adjacent work, or thin but real signal. |
| 2 | Weak / adjacent / soft aspiration; skill barely evidenced in the snippet. |
| 1 | Trace mention only (unused in first run; treat as below 2). |
| — | No mappable skill signal. |

### Calibration anchors from frozen run (do not rescore these)
- **4**: customer-system DSL integration → `api-auth`; bank requirements→integrate → `cust-discovery`/`api-auth`/`legacy-data`; FDE interview prep as decomp gate → `ambiguity-decomp`; FDE as consultant/SE → `exec-comm`; lead AI SE implement apps → `llm-integrate` + decomp.
- **3**: FDE role mix listing customer + architecture + integration + small prototypes; CV/artifact expectations; per-customer config scope; IDP PoC / platform stack → `cloud-deploy`.
- **2**: career-adjacent musing; title framing with thin skill detail; PoC-for-learning (not live prod) → `prod-ship` 2; soft SA aspiration.
- **prod-ship bar**: small prototypes in role mix = 3 (below live-prod); learning/pitch PoC = 2; live production ownership would be higher.

## Rollup
- Per competency, **max demand** across items in the run.
- List high-demand IDs (typically ≥ 4) and full per-item table.

## Flag rule (unchanged)
- Flag when **demand ≥ 4** AND Lucas **evidence ≤ 2**.
- If evidence is a range (e.g. `2-3`), flag **only if the high end ≤ 2**.
- Example frozen: `llm-integrate` demand 4, evidence `2-3` → **not flagged**.

## Output contract
- Update `/workspace/context/signals.md` with run summary, flags, demand rollup, per-item demand, unmapped list.
- Never edit competencies.md evidence/target.
- Never edit plan.md or propose a learning plan from scoring alone.
