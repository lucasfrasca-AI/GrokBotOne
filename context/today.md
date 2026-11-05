# Today's single target
# Owner: Mentor. One target only. Not a plan version.

- **date**: 2026-11-05 (Sydney) — week 8, day 4 (plan v013)
- **stage**: 3 — Infrastructure / Hosting (plan v013), week 8
- **competency**: `api-auth`
- **lane**: build
- **from plan**: v013 week 8 Thu — third and last api-auth day (Tue–Thu)
- **calendar**: Mon cloud-deploy close-out (cap spent; completion not recorded) → Tue–Thu api-auth → Fri prod-ship; week 9 overflow only if week-8 artifact confirmed not done
- **work**: Finish the one authenticated API boundary: token issue/verify working on the baseline (or smallest single-region) endpoint, with the reject path actually returning 401/403. No new cloud-deploy work.
- **why**: Stayed — last of v013's three api-auth days (Fri moves to prod-ship) and it's still flagged (demand 4, evidence 2); no completion recorded yet
- **diagram archetype**: `sequence` — client → auth (token issue/verify) → API endpoint, trust boundary marked, reject path shown
- **sources**: historical Reddit run 20260906T231515Z only (captures 03, 13, 02); fresh Scout run still pending
- **deferred tagged here**: none (deferred/api-auth.md is empty)
