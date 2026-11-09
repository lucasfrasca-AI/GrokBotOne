# Today's single target
# Owner: Mentor. One target only. Not a plan version.

- **date**: 2026-11-09 (Sydney) — week 9 overflow, day 1 (plan v014)
- **stage**: 3 — Infrastructure / Hosting (plan v014), week 9 overflow
- **competency**: `api-auth`
- **lane**: build
- **from plan**: v014 week 9 Mon — finish the authenticated API boundary; standing-endpoint gate first if the baseline is not standing
- **calendar**: Mon–Wed `api-auth` (today; standing-endpoint gate first if needed) → Thu–Fri `prod-ship`; no week 10; stage 4 does not start
- **work**: If the baseline still isn't standing, cut to the smallest deployable single-region endpoint (no more design). Then implement the authenticated API boundary on that endpoint: valid tokens accepted, missing or invalid tokens rejected (401/403).
- **why**: Moved — week 9 overflow opened because the week-8 baseline and `api-auth` completion still aren't recorded; v014's first pick is `api-auth`, with the standing-endpoint scope-cut if the baseline isn't up
- **diagram archetype**: `sequence` — client request hits the endpoint, the token is checked, and the path splits to 200 or 401/403
- **sources**: historical Reddit run 20260906T231515Z only (captures 03, 13, 02); fresh Scout run still pending
- **deferred tagged here**: none (deferred/api-auth.md is empty)
