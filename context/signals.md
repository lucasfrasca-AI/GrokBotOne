# FDE market signals
# Owner: Analyst. Source run: Lurk Reddit 20260906T231515Z (15 items).
# Demand scored 2026-09-07 against rebuilt competencies.md. Flags applied after Lucas filled evidence.
# Demand 1–5 only in this file. Evidence/target read from competencies.md for flags — never written back.

## Run summary
- **source**: reddit `/workspace/captures/reddit/`
- **run_id**: `20260906T231515Z`
- **items scored**: 15
- **matrix**: rebuilt IDs; Lucas evidence+target final
- **flag rule**: demand ≥ 4 AND Lucas evidence ≤ 2 (ranges: flag only if high end ≤ 2)

## Flags
| competency | demand | Lucas evidence | why |
|------------|--------|----------------|-----|
| api-auth | 4 | 2 | Customer-system / bank integration (03, 13) |
| cust-discovery | 4 | 1 | Implementation engineer requirements path (13); SE/FDE framing (11, 12) |
| ambiguity-decomp | 4 | 2 | AI SE role → plan (12); FDE interview prep (07) |
| exec-comm | 4 | 1 | FDE as consultant/sales-facing (11) |
| legacy-data | 4 | 1 | Bank systems integrate/configure/custom APIs (13) |

Not flagged despite demand ≥ 4:
- **llm-integrate** — demand 4, Lucas evidence `2-3` (high end > 2)

## Demand rollup (this run)
| competency | max demand | Lucas evidence | flagged? |
|------------|------------|----------------|----------|
| api-auth | 4 | 2 | YES |
| cust-discovery | 4 | 1 | YES |
| llm-integrate | 4 | 2-3 | no |
| ambiguity-decomp | 4 | 2 | YES |
| exec-comm | 4 | 1 | YES |
| legacy-data | 4 | 1 | YES |
| scope-write | 3 | 2 | no (demand < 4) |
| prod-ship | 3 | 2 | no |
| cloud-deploy | 3 | 2-3 | no |
| enterprise-auth | — | 2 | no signal |
| compliance-deploy | — | 3 | no signal |
| prod-lang | — | 1-2 | no signal |
| codebase-debug | — | 1 | no signal |
| context-eng | — | 3 | no signal |
| agent-orch | — | 3 | no signal |
| eval-design | — | 2 | no signal |
| prod-ownership | — | 1 | no signal |

## Per-item demand (new IDs only)
| # | file stem | competency | demand | note |
|---|-----------|------------|--------|------|
| 01 | thinking-of-backup-plans | cloud-deploy | 2 | Weak career-adjacent SA/DevOps/security musing |
| 02 | forward-deployed-engineer-role | cust-discovery | 3 | Customer-facing + technical mix |
| 02 | (also) | api-auth | 3 | Integration called out in role mix |
| 02 | (also) | prod-ship | 3 | Small prototypes — below live-prod bar |
| 02 | (also) | ambiguity-decomp | 3 | Architecture/problem shaping implied |
| 03 | forward-deployed-engineer-roles-seem-like-a-scam | api-auth | 4 | In-house DSL to integrate product with customer systems |
| 03 | (also) | legacy-data | 3 | Customer-system integration wall |
| 04 | why-the-sudden-popularity-of-forward-deployed-engineer-again | — | — | Meta hiring/title chatter; no skill ID |
| 05 | what-is-the-hiring-process-for-forward-deployment-engineers- | — | — | Hiring-process meta; no skill ID |
| 06 | guidance-on-becoming-a-forward-deployed-engineer | — | — | Career-transition meta; no skill ID |
| 07 | engineers-hiring-managers-how-should-i-prepare-for-forward-d | ambiguity-decomp | 4 | Prep for FDE interviews (decomp round is the signature gate) |
| 07 | (also) | scope-write | 3 | CV / written-artifact expectations implied |
| 07 | (also) | exec-comm | 3 | Customer-facing interview signal thin in snippet |
| 08 | is-forward-deployed-engineer-the-next-hot-thing | — | — | Hiring-volume meta; no skill ID |
| 09 | i-keep-seeing-forward-deployed-engineer-openings-what-s-the- | — | — | Openings/background meta; no skill ID |
| 10 | managers-you-ve-been-promoted-to-forward-deployed-engineer | exec-comm | 2 | Title framing in devops; thin skill detail |
| 11 | what-do-you-think-about-new-emerging-role-forward-deployed-e | exec-comm | 4 | Framed as consultant / sales engineer |
| 11 | (also) | cust-discovery | 3 | Customer-facing discovery implied |
| 12 | new-job-as-a-lead-ai-solutions-engineer-i-m-not-even-sure-wh | llm-integrate | 4 | Lead AI enablement / implement applications |
| 12 | (also) | ambiguity-decomp | 4 | Role unclear; must turn vague AI mandate into a plan |
| 12 | (also) | cust-discovery | 3 | Discover where AI actually helps |
| 12 | (also) | exec-comm | 3 | Org-wide enablement stakeholders |
| 13 | what-is-the-role-of-an-implementation-engineer-should-a-fres | cust-discovery | 4 | Bank requirements → configure/integrate |
| 13 | (also) | api-auth | 4 | Custom APIs / system integration |
| 13 | (also) | legacy-data | 4 | Bank server/system integration wall |
| 13 | (also) | scope-write | 3 | Per-customer change/config scope |
| 14 | building-an-idp-poc-for-self-learning-and-potential-pitch-wh | cloud-deploy | 3 | IDP PoC / modern platform stack |
| 14 | (also) | prod-ship | 2 | Explicit PoC for learning/pitch — not live production ownership |
| 15 | stay-where-i-am-move-or-wait | exec-comm | 2 | Soft SA aspiration; weak skill pull |
| 15 | (also) | scope-write | 2 | Consulting → SA path; thin |

## Unmapped this run
Items 04, 05, 06, 08, 09 are FDE title/hiring meta. Retired `market-fit` covered them; no replacement ID on the rebuilt matrix — left unmapped rather than forced.

## Not touched
- Did not edit competencies.md (evidence/target untouched)
- Did not edit plan.md
- Did not propose a learning plan
