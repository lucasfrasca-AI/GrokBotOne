# Today's single target
# Owner: Mentor. One target only. Not a plan version.

- **date**: 2026-11-06 (Sydney) — week 8, day 5 (plan v013)
- **stage**: 3 — Infrastructure / Hosting (plan v013), week 8
- **competency**: `prod-ship`
- **lane**: build
- **from plan**: v013 week 8 Fri — run the baseline + auth boundary under real use, record what broke
- **calendar**: Mon cloud-deploy close-out → Tue–Thu api-auth → Fri prod-ship (today); week 9 overflow only if Lucas/Mentor confirm the week-8 artifact isn't done
- **work**: Put the deployed endpoint with its auth boundary under real use (real calls, valid and rejected tokens), fix what breaks, and write a short "what broke / what I changed" log. No new design or cloud-deploy work.
- **why**: Moved — api-auth's three days (Tue–Thu) are spent per v013, and Friday shifts to keeping the baseline live; no api-auth or baseline completion recorded, so week-9 overflow may open
- **diagram archetype**: `timeline` — request run over the day: deploy → real calls → failures/incidents → fixes, with the 401/403 reject path marked
- **sources**: historical Reddit run 20260906T231515Z only (captures 02, 14, 13); fresh Scout run still pending
- **deferred tagged here**: none (deferred/prod-ship.md is empty)
