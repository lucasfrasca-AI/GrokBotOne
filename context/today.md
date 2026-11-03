# Today's single target
# Owner: Mentor. One target only. Not a plan version.

- **date**: 2026-11-03 (Sydney) — week 8, day 2 (plan v013)
- **stage**: 3 — Infrastructure / Hosting (plan v013), week 8
- **competency**: `api-auth`
- **lane**: build
- **from plan**: v013 week 8 Tue — first of three api-auth days (Tue–Thu)
- **calendar**: Mon cloud-deploy close-out (cap spent; completion not recorded) → Tue–Thu api-auth → Fri prod-ship; week 9 overflow only if week-8 artifact confirmed not done
- **work**: Wire one authenticated API boundary onto the baseline endpoint (implemented, not only drawn). If Monday's baseline isn't standing, put the auth boundary on the smallest single-region endpoint per v013's cut rule — no extra cloud-deploy day.
- **why**: Moved — Monday's one-day cloud-deploy cap is spent, so v013 hands Tue–Thu to api-auth, which is also flagged (demand 4, evidence 2); baseline completion still unrecorded
- **diagram archetype**: `sequence` — client → auth (token issue/verify) → API endpoint, trust boundary marked, reject path shown
- **sources**: historical Reddit run 20260906T231515Z only (captures 03, 13, 02); fresh Scout run still pending
- **deferred tagged here**: none (deferred/api-auth.md is empty)
