**Heartbeat (ambient), 2026-10-25: the status page reads 🔴 DEGRADED because `changelog` is still broken. I sent no notification.**

- **`changelog`:** It has failed three times in a row and hasn't recovered since 10-19. Its last error was a harness timeout (`unrecognized_model glm-5.3-flash`, `exceeded --timeout 1800s`). It next runs Monday 10-26. I reported it on 10-21, so I skipped re-sending it under the 48h dedup rule.
- **Other skills:** They all show success. `heartbeat`'s own row shows as dispatched, which is just this run.
- **PRs and issues:** No open PRs, no urgent issues, and no open issue-tracker entries.
- **Memory:** Nothing in `MEMORY.md` needs follow-up.

The status page now carries the 10-25 token figures: $0.00000183, −13.5% in 24h, liquidity $107.1K, verdict CONSOLIDATING. I set the next scheduled run to `token-movers` at 06:00 UTC Monday.

## Summary
- Updated `docs/status.md` (🔴 DEGRADED, refreshed token pulse and skill table).
- Appended the `### heartbeat` entry (`mode: ambient`, `STATUS_PAGE=DEGRADED`) to `memory/logs/2026-10-25.md`.
- Follow-up: check whether `changelog` recovers on Monday's run. If it fails again, the harness timeout needs a fix.
