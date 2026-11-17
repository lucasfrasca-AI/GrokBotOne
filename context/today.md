# Today's single target
# Owner: Mentor. One target only. Not a plan version.

- **date**: 2026-11-17 (Sydney) — week 10 close-out, day 2 (plan v015)
- **stage**: 3 — Infrastructure / Hosting (plan v015), week 10 final close-out
- **competency**: `api-auth`
- **lane**: build
- **from plan**: v015 week 10 Tue–Wed — authenticated boundary on that endpoint
- **calendar**: Mon `cloud-deploy` evidence day → Tue–Wed `api-auth` → Thu–Fri `prod-ship`; Stage 3 closes Fri 2026-11-20 regardless; no week 11; next rewrite Sun 2026-11-22
- **work**: Standing-endpoint gate first if the baseline is not standing (smallest single-region endpoint, not more design), then the authenticated API boundary on that endpoint.
- **why**: Moved — Tuesday opens the Tue–Wed `api-auth` window after Monday's `cloud-deploy` evidence day; neither the authenticated API boundary nor a standing baseline is recorded as done
- **diagram archetype**: `sequence` — request lifecycle across the authenticated API boundary
- **sources**: historical Reddit run 20260906T231515Z only (captures 03, 13, 02); fresh Scout run still pending
- **deferred tagged here**: none (deferred/api-auth.md is empty)
