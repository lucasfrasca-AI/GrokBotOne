# Today's single target
# Owner: Mentor. One target only. Not a plan version.

- **date**: 2026-11-10 (Sydney) — week 9 overflow, day 2 (plan v014)
- **stage**: 3 — Infrastructure / Hosting (plan v014), week 9 overflow
- **competency**: `api-auth`
- **lane**: build
- **from plan**: v014 week 9 Tue — finish the authenticated API boundary; standing-endpoint gate first if the baseline is not standing
- **calendar**: Mon–Wed `api-auth` (today; standing-endpoint gate first if needed) → Thu–Fri `prod-ship`; no week 10; stage 4 does not start
- **work**: If the baseline still isn't standing, cut to the smallest deployable single-region endpoint (no more design). Then implement the authenticated API boundary on that endpoint: valid tokens accepted, missing or invalid tokens rejected (401/403).
- **why**: Stayed — week 9 overflow day 2 is still inside v014's Mon–Wed `api-auth` window; neither the authenticated API boundary nor a standing baseline is recorded as done since yesterday's pick
- **diagram archetype**: `sequence` — client request hits the endpoint, the token is checked, and the path splits to 200 or 401/403
- **sources**: historical Reddit run 20260906T231515Z only (captures 03, 13, 02); fresh Scout run still pending
- **deferred tagged here**: none (deferred/api-auth.md is empty)
