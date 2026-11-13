# Today's single target
# Owner: Mentor. One target only. Not a plan version.

- **date**: 2026-11-13 (Sydney) — week 9 overflow, day 5 (plan v014)
- **stage**: 3 — Infrastructure / Hosting (plan v014), week 9 overflow
- **competency**: `prod-ship`
- **lane**: build
- **from plan**: v014 week 9 Fri — keep the baseline running under real use
- **calendar**: Mon–Wed `api-auth` → Thu–Fri `prod-ship` (today, last day); no week 10; stage 4 does not start; next rewrite Sun 2026-11-15
- **work**: Keep the baseline running under real use: debug and iterate against a live endpoint, not a disposable lab. If the baseline still isn't standing, cut to the smallest deployable single-region endpoint that can take real use (no more design).
- **why**: Stayed — Friday is still inside v014's Thu–Fri `prod-ship` window (week 9 overflow day 5, last day); neither the authenticated API boundary nor a standing baseline is recorded as done since yesterday's pick
- **diagram archetype**: `sequence` — ship → observe under real usage → debug → iterate, ownership stays on the loop
- **sources**: historical Reddit run 20260906T231515Z only (captures 02, 14, 13); prod-ship demand max 3 — thin; fresh Scout run still pending
- **deferred tagged here**: none (deferred/prod-ship.md is empty)
