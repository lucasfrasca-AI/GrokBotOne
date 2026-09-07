# FDE competency matrix
# Owner: Mentor (IDs + definitions). Evidence and target: Lucas only — never overwritten by Mentor or Analyst.
# Rebuilt 2026-09-07 from Lucas’s 2026 role research. Scores written 2026-09-07 exactly as Lucas provided.
# Analyst scores market demand against these IDs only. Never write evidence or target.

## Scale (Lucas)
5 — shipped it repeatedly, could walk someone through the hard parts
4 — shipped it once in production, it held up
3 — done it, but in a small or forgiving context
2 — read about it, maybe a prototype
1 — no

## CORE ENGINEERING

| id | competency | what good looks like | evidence | target |
|----|------------|----------------------|----------|--------|
| prod-ship | Shipping and maintaining live production systems | The hard gate. Not projects — systems kept running, debugged and iterated under real usage. | 2 | 4-5 |
| prod-lang | Depth in one production language | Python is the AI-adjacent baseline; depth matters more than which. | 1-2 | 4-5 |
| cloud-deploy | Cloud platform working knowledge | AWS / Azure / GCP working knowledge. | 2-3 | 4-5 |
| codebase-debug | Debugging an unfamiliar codebase | Debug without the original author. | 1 | 4 |
| api-auth | API integration and authentication patterns | Solid API + auth patterns in real systems. | 2 | 5 |

## APPLIED AI

| id | competency | what good looks like | evidence | target |
|----|------------|----------------------|----------|--------|
| llm-integrate | LLM integration in production systems | LLMs wired into live systems, not demos. | 2-3 | 5 |
| context-eng | Context engineering | RAG, vector DBs, knowledge graphs, embeddings, chunking, reranking, memory — what the model sees at inference, and how it got there. | 3 | 5 |
| agent-orch | Agent orchestration and harness design | Where Claude Skills captures belong. | 3 | 5* |
| eval-design | Eval suites | Catch hallucination and regression. Non-negotiable at frontier labs. | 2 | 5 |

## INTEGRATION WALL

| id | competency | what good looks like | evidence | target |
|----|------------|----------------------|----------|--------|
| legacy-data | Legacy databases, ETL, migration | Legacy DBs, ETL pipelines, data migration in customer environments. | 1 | 4 |
| enterprise-auth | Enterprise SSO | OIDC, SAML. | 2 | 4 |
| compliance-deploy | Compliance in customer deploy | Data residency, regulatory constraints, security sign-off in customer environments. | 3 | 5 |

## CUSTOMER-FACING

| id | competency | what good looks like | evidence | target |
|----|------------|----------------------|----------|--------|
| ambiguity-decomp | Decomposing an ambiguous customer problem | Into a plan. Signature interview round; ~40% pass rate; weighted above coding. | 2 | 4 |
| cust-discovery | Customer discovery | Drawing out the real problem behind the stated one. | 1 | 4 |
| exec-comm | Exec communication | Technical tradeoffs to skeptical non-technical stakeholders, without losing precision. | 1 | 5 |
| prod-ownership | Production ownership | Staying with a system through its failures, not just its launch. | 1 | 5 |
| scope-write | Scoping & engagement artifacts | Scoping and written engagement artifacts. | 2 | 5 |

## Notes
- Evidence and target are Lucas-final. Never overwrite. If a cell is blank, leave blank and tell Lucas — never guess.
- Analyst: demand column in signals.md only. Never write evidence or target here.
- Never invent public content from this matrix.
