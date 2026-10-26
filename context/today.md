# Today's single target
# Owner: Mentor. One target only. Not a plan version.

- **date**: 2026-10-26 (Sydney) — week 7 gate day
- **stage**: 3 — Infrastructure / Hosting (plan v012), week 7
- **competency**: `cloud-deploy`
- **lane**: build
- **from plan**: v012 stage 3 week 7 gate — if the IaC baseline isn't standing, the first week-7 pick closes it on cloud-deploy before api-auth starts
- **calendar**: Week 7 Mon 26 → Fri 30 Oct authenticated API boundary (api-auth) after gate; week 8 Mon 2 → Fri 6 Nov keep baseline running (prod-ship)
- **work**: Close out the decision record and get the IaC hosting baseline actually deployed and reachable, so the api-auth boundary has something real to attach to
- **why**: Neither a finished decision record nor a running baseline is recorded, so v012's gate holds cloud-deploy one more day before api-auth
- **diagram archetype**: `architecture` — use case → hosting tier → provider/region, trust boundary marked, API entry point stubbed
- **sources**: historical Reddit run 20260906T231515Z only (captures 14, 13, 03); fresh Scout run still pending
- **deferred tagged here**: none (deferred/cloud-deploy.md and deferred/api-auth.md are empty)
