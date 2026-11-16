# Today's single target
# Owner: Mentor. One target only. Not a plan version.

- **date**: 2026-11-16 (Sydney) — week 10 close-out, day 1 (plan v015)
- **stage**: 3 — Infrastructure / Hosting (plan v015), week 10 final close-out
- **competency**: `cloud-deploy`
- **lane**: build
- **from plan**: v015 week 10 Mon — evidence day: record what exists (decision record, reachable endpoint, auth path); if nothing is standing, ship the smallest single-region endpoint today
- **calendar**: Mon `cloud-deploy` evidence day → Tue–Wed `api-auth` → Thu–Fri `prod-ship`; Stage 3 closes Fri 2026-11-20 regardless; no week 11; next rewrite Sun 2026-11-22
- **work**: Record what actually exists (decision record, reachable endpoint, auth path). If nothing is standing, ship the smallest deployable single-region endpoint today (no more design).
- **why**: Moved — week 10 (v015) opens today as Stage 3's hard-capped close-out, so the pick moves off Friday's `prod-ship` onto Monday's `cloud-deploy` evidence day; neither the authenticated API boundary nor a standing baseline is recorded as done
- **diagram archetype**: `architecture` — hosting baseline: provider, region, compute, networking, and the reachable endpoint
- **sources**: historical Reddit run 20260906T231515Z only (captures 01, 14); cloud-deploy demand max 3 — thin; only two scored captures, third pending; fresh Scout run still pending
- **deferred tagged here**: none (deferred/cloud-deploy.md is empty)
