# Learning Plan — v016

- **Written:** 2026-11-22 (AEST)
- **Owner:** Curriculum (reports to Mentor)
- **Prior:** v015
- **Status:** active — FDE 11-stage map as syllabus spine; cycle 1 (stages 1–3) **closed** Fri 2026-11-20; cycle 2 = stages 4–5
- **Trigger:** standing Sunday 18:00 AEST rewrite (no two-run Mentor gap)

## Syllabus spine (Lucas, 2026-09-12)

Work in the order it happens. Matrix IDs score progress; this map sets sequence.

| # | phase | stage |
|---|-------|-------|
| 1 | PLAN | Discovery / Design — Use Case, Success Metrics, Readiness, Business Case |
| 2 | PLAN | Compliance — Data Sovereignty, Privacy, Regulation, Risk Management |
| 3 | BUILD | Infrastructure / Hosting — Solution Architecture, Hosting Model, Cloud Provider, Compute, Networking, Interfaces, IaC |
| 4 | BUILD | Data Pipeline — Retrieval Strategy, Sources, Ingestion, Chunking, Storage, Retrieval Techniques |
| 5 | BUILD | Model Configuration — Access, Selection, Customisation, Prompt / Context Engineering, Inference Parameters |
| 6 | BUILD | Orchestration / Harness — Agent Patterns, Frameworks, Tool Calling, Memory, Caching, Resilience, Human-in-the-Loop |
| 7 | BUILD | Security / Guardrails — Input Controls, Data Protection, Access Control, Output Controls, Abuse Prevention |
| 8 | VALIDATE | Evaluation / Tuning — Quality Metrics, Bias, Eval Methods, Adversarial Testing, Tuning Loop, Tooling, Acceptance |
| 9 | RUN | Visibility / LLMOps — Interpretability, Cost, Performance, Quality Monitoring, Audit, Observability |
| 10 | RUN | Deployment / Lifecycle — Deployment, Versioning, Change Control, Continuous Improvement, Operations |
| 11 | RUN | Adoption / Hand Off — Stakeholders, Enablement, Hand Off, Value Realisation |

**Cycle 1 (stages 1–3) is closed. Cycle 2 covers stages 4–5 only.** Stages 6–11 sit in **Later cycles** below.

## Rationale

Standing Sunday rewrite, and the one v015 committed to: Stage 3's hard-capped week 10 (Mon 2026-11-16 → Fri 2026-11-20) has ended, so this version closes cycle 1 and decides what opens next. Inputs are unchanged since v015 — competencies.md evidence/targets are as Lucas wrote them on 2026-09-07, `/workspace/captures` holds only the historical Reddit run `20260906T231515Z`, and `signals.md` is still that single run with Mentor's fresh Scout run pending (`today.md` 2026-11-20) — so no Mentor-flagged gap has persisted across two runs and nothing is reshaped on demand grounds. Mentor's last pick (Fri 2026-11-20, `prod-ship`) again records neither the authenticated API boundary nor a standing baseline as done, and Lucas has recorded no completion for the Stage 1 pack, Stage 2 pack, decision record or baseline. As v015 promised, there is **no week 11**: cycle 1 closes with an explicit debt ledger, and cycle 2 opens on **stage 4 (Data Pipeline) then stage 5 (Model Configuration)**, Mon 2026-11-23 → Fri 2026-12-18. Rather than a cycle reset that would re-run stages 1–3 on the same calendar pattern that produced ten weeks without a recorded artifact, v016 makes the debt payable *inside* the new build: the stage 4 pipeline must ingest from the stage-1 use case's sources and serve retrieval from **one deployed, reachable endpoint behind one auth check**, so a working stage 4 artifact also clears the Stage 3 baseline and `api-auth` debt. Each week opens with a short Monday evidence check (≤30 min, not a full day) where Lucas records what exists; Curriculum still invents no completions. Study stays at 30% (retrieval/chunking patterns in week 1, model access/selection in week 3) and build at 70% inside stages 4–5.

**Deliberately not covering this cycle:** orchestration, security/guardrails, evaluation, LLMOps, deployment/lifecycle, adoption/hand-off (stages 6–11). No re-run of stages 1–3 as their own weeks — their unfinished artifacts are carried as debt and closed either by Lucas recording them or inside the stage 4–5 build. Deep `enterprise-auth` (SSO/OIDC/SAML) waits for stage 7; one simple auth check on the endpoint is enough here. Interview-only drills without a stage artifact are out.

Numbers: where Lucas gave a range, the **lower** figure is used and marked provisional until he confirms.

## Operating rules

1. Hold a **30% study / 70% build** split **inside the active cycle's stages (4–5)** — not across the full map or matrix.
2. Never edit a written plan version. Always add a new numbered version with a diff and a one-paragraph rationale.
3. Canonical latest: `/workspace/context/plan.md`. Snapshots: `/workspace/context/plan/vNNN.md` (+ `.diff`).
4. Mentor picks **one** daily target from the active stage (or its study slice). Curriculum does not set the day-of pick.
5. Each new version goes to Mentor and Herald.
6. Evidence and targets are Lucas-only — never invent or overwrite scores.
7. Gap rewrites: when a Mentor-flagged gap in `signals.md` persists across two runs; Sunday 18:00 AEST rewrite regardless. (Analyst is retired.)
8. Debt rule (new): cycle-1 debt is closed by Lucas recording it, or by the stage 4–5 artifact running on a deployed, authenticated endpoint. No stage is reopened as its own calendar week.

## Score convention (floored)

| id | evidence | target | notes |
|----|----------|--------|-------|
| context-eng | 3 | 5 | as written — stage 4 primary |
| legacy-data | 1 | 4 | as written — stage 4 (sources/ingestion); one-run Mentor flag |
| llm-integrate | 2 | 5 | evidence floored from `2-3` — provisional; stage 5 primary |
| cloud-deploy | 2 | 4 | floored from `2-3` / `4-5` — provisional; cycle-1 debt |
| prod-ship | 2 | 4 | target floored from `4-5` — provisional; cycle-1 debt |
| api-auth | 2 | 5 | as written; cycle-1 debt; one-run Mentor flag |

Cycle-1 IDs not carried as primaries (`cust-discovery`, `ambiguity-decomp`, `scope-write`, `exec-comm`, `compliance-deploy`) are unchanged in competencies.md and reappear at stages 7 and 11.

## Cycle 1 close-out — debt ledger (as of 2026-11-22 AEST)

| artifact | stage | calendar | recorded status | how it closes |
|----------|-------|----------|-----------------|---------------|
| Discovery + scoping pack | 1 | Mon 2026-09-14 → Fri 2026-09-25 | not recorded | Lucas records it exists, or writes a one-page use-case statement in week 1 Mon check (the stage 4 sources depend on it) |
| Compliance & risk pack | 2 | Mon 2026-09-28 → Fri 2026-10-09 | not recorded | Lucas records it; else the stage 4 storage choice notes its residency position in one paragraph |
| Decision record (architecture) | 3 | weeks 5–6 | not recorded | Lucas records it; else written as the stage 4 pipeline's hosting note |
| IaC baseline, deployed and reachable | 3 | weeks 6–10 | not recorded | stage 4 week 1: pipeline served from one deployed single-region endpoint |
| Authenticated API boundary | 3 | weeks 7–10 | not recorded | stage 4 week 2: one auth check on the retrieval endpoint |
| Baseline kept running + run log | 3 | weeks 8–10 | not recorded | carried through cycle 2: endpoint stays up; short run log each Friday |

## This cycle — stages 4 to 5

### Study / build allocation (inside 4–5 only)

| Lane | Share | Where it sits |
|------|-------|---------------|
| Study | 30% | Week 1: retrieval strategy, chunking, storage options. Week 3: model access, selection, prompt/context patterns |
| Build | 70% | The two shippable artifacts below, on the deployed endpoint |

### Stage 4 — Data Pipeline (BUILD)

**Ship:** a **working retrieval pipeline** for the stage-1 use case — real sources ingested, chunked, stored, and retrievable through **one deployed, authenticated endpoint**, with a short note on retrieval strategy and why. Not a notebook.

| moves | evidence→target | how the artifact moves it |
|-------|-----------------|---------------------------|
| context-eng | 3 → 5 | Chunking, storage and retrieval choices made and implemented for a real source set |
| legacy-data | 1 → 4 | Ingestion from at least one messy/structured customer-style source (DB export, CSV, legacy API) |
| cloud-deploy / prod-ship / api-auth | debt | Served from a deployed endpoint behind one auth check, kept running |

| week | calendar (AEST) | focus | primary id |
|------|-----------------|-------|------------|
| 1 | Mon 2026-11-23 → Fri 2026-11-27 | Mon: ≤30 min evidence check (record what exists from cycle 1). Mon–Tue: study open (retrieval/chunking/storage). Wed–Fri: ingest + chunk + store one source set; serve retrieval from the smallest single-region endpoint | `context-eng` → `cloud-deploy` (debt) |
| 2 | Mon 2026-11-30 → Fri 2026-12-04 | Add one legacy-style source; add one auth check on the endpoint; Fri run log | `legacy-data` → `api-auth` (debt) |

### Stage 5 — Model Configuration (BUILD)

**Ship:** the stage 4 pipeline **wired to a model** — chosen access path and model with a short selection note, a versioned prompt/context template, and recorded inference parameters, answering real queries from the endpoint.

| moves | evidence→target | how the artifact moves it |
|-------|-----------------|---------------------------|
| llm-integrate | 2 → 5 | LLM wired into the live pipeline, not a demo |
| context-eng | 3 → 5 | Prompt/context engineering over the stage 4 retrieval |
| prod-ship | debt | Endpoint kept running under use; Friday run logs |

| week | calendar (AEST) | focus | primary id |
|------|-----------------|-------|------------|
| 3 | Mon 2026-12-07 → Fri 2026-12-11 | Mon–Tue: study open (model access/selection, prompt patterns). Wed–Fri: wire model to retrieval; selection note | `llm-integrate` |
| 4 | Mon 2026-12-14 → Fri 2026-12-18 | Prompt/context template versioned; inference params recorded; keep endpoint up; Fri run log + cycle 2 close | `context-eng` → `prod-ship` |

Sequencing guide only — Mentor still picks one target per day and may reorder on evidence. Split check: 3 study days of 20 (15%) plus targeted reading when a build step blocks, capped at 30%; build ≥70%. **Cycle 2 closes Fri 2026-12-18**; the rewrite on Sun 2026-12-20 plans the holiday break and cycle 3.

### Cycle history

| cycle | calendar (AEST) | stages | status |
|-------|-----------------|--------|--------|
| 1 | Mon 2026-09-14 → Fri 2026-11-20 (weeks 1–10) | 1–3 | **closed** — calendar complete; no artifact completion recorded; debt ledger above |
| 2 | Mon 2026-11-23 → Fri 2026-12-18 (weeks 1–4) | 4–5 | **active** — opens Mon 2026-11-23 |

## Mentor flags caveat

Current `signals.md` still reflects a single historical Reddit scoring run (pre-Mentor ownership, `20260906T231515Z`); Mentor's 2026-11-20 `today.md` says a fresh Scout run is still pending. Persistence rewrite still waits for a **second confirming Mentor run** against the same gap. One-run flags remain: `api-auth`, `cust-discovery`, `ambiguity-decomp`, `exec-comm`, `legacy-data`. Cycle 2 directly works `legacy-data` and `api-auth`. Sunday 18:00 AEST rewrite remains standing.

## Later cycles (stages 6–11)

Visible. Not planned this cycle. Competency hints are directional only.

| # | stage | primary matrix IDs (indicative) |
|---|-------|----------------------------------|
| 6 | Orchestration / Harness | `agent-orch` |
| 7 | Security / Guardrails | `compliance-deploy`, `api-auth`, `enterprise-auth` |
| 8 | Evaluation / Tuning | `eval-design` |
| 9 | Visibility / LLMOps | `prod-ship`, `prod-ownership` |
| 10 | Deployment / Lifecycle | `prod-ship`, `prod-ownership`, `cloud-deploy` |
| 11 | Adoption / Hand Off | `exec-comm`, `scope-write`, `cust-discovery` |

Also deferred as standalone P0s unless a later stage pulls them in: `prod-lang`, `codebase-debug`, deep `enterprise-auth` (until stage 7), `eval-design` / `agent-orch` (until stages 6–8), `prod-ownership` as its own arc (until stages 9–10).

## Diff vs v015

- Standing Sunday rewrite; no priority reshape on demand grounds (no two-run Mentor gap; Scout run still pending per Mentor 2026-11-20)
- Stage 3 week 10 marked done; **cycle 1 (stages 1–3) closed** Fri 2026-11-20 with no artifact completion recorded; no week 11
- Added a cycle-1 **debt ledger** (Stage 1 pack, Stage 2 pack, decision record, baseline, auth boundary, run log) and debt rule 8: debt closes by Lucas recording it or inside the stage 4–5 build on a deployed, authenticated endpoint
- **Cycle 2 opened: stage 4 Data Pipeline (weeks 1–2, Mon 2026-11-23 → Fri 2026-12-04) then stage 5 Model Configuration (weeks 3–4, Mon 2026-12-07 → Fri 2026-12-18)**
- Score table now: `context-eng` 3→5, `legacy-data` 1→4, `llm-integrate` 2→5 (floored), plus `cloud-deploy` / `prod-ship` / `api-auth` as debt; no scores changed in competencies.md
- 30/70 split now held inside stages 4–5; Monday evidence check capped at 30 min; Later cycles now stages 6–11
