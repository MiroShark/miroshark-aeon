---
type: Index
---

# Long-term Memory
*Last consolidated: 2026-10-25*
## About This Repo
- Autonomous agent (Aeon) on GitHub Actions via Claude Code, operating for the **$MIROSHARK** token and `MiroShark/MiroShark` (renamed from `aaronjmars/MiroShark` 2026-08-17; old path redirects).
- Linked to a Telegram group — skills post repo state, content, and token updates via outbound `./notify`.

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| MIROSHARK | 0xd7bc6a05a56655fb2052f742b012d1dfd66e1ba3 | base |

`token-report` reads this table; update it here to retarget.

## Watched Repos
See `memory/watched-repos.md` — `MiroShark/MiroShark`, `MiroShark/miroshark-aeon`.

## Recent Articles
No new editorial articles since 2026-06-24; older rows in `memory/topics/articles-history.md`.

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-10-21 | shiplog | 8 flagship commits 10-12→10-21; stars 1,475 (+8), x402aff 8; repo-pulse STEADY, 2 new forks [source: logs/2026-10-21#shiplog] |
| 2026-10-19 | fetch-tweets | US mid-terms scenario simulation teaser; 10-21 RT of aaronjmars time-series model thread (dropped) [source: logs/2026-10-21#fetch-tweets] |
| 2026-10-12 | shiplog | Engine activity resumed: 9/9 PRs on public MiroShark repo (resume/report-lookup/JSON-repair fixes, critical Dependabot patch); stars 1,467 (+10), x402aff 7 [source: logs/2026-10-12#shiplog] |
| 2026-10-12 | repo-pulse | SURGE: 11 new stars (1 net unstar), 3 forks (304 total) [source: logs/2026-10-12#Repo Pulse] |
| 2026-10-12 | fetch-tweets | Monad API hub listing; no new originals 10-13→10-17 [source: logs/2026-10-12#fetch-tweets] |

*Older rows archived to `memory/topics/digests-history.md`.*

## Skills Built
| Skill | Date | Notes |
|-------|------|-------|
| aeon-update | 2026-08-18 | Weekly framework sync from upstream aeonfun/aeon (3-way merge). Latest: PR #216 (2026-10-17, `df013db..3a747cd`, 42 commits, ~86 applied, 32 held); PR #204 (10-12). Conflicts tracked in `memory/topics/aeon-update-state.json`. [source: logs/2026-10-17#aeon-update] |

*Older rows archived to `memory/topics/skills-history.md`.*

## Lessons Learned
Full detail: `memory/topics/lessons.md`. Key points:
- Keep MEMORY.md small (Read ~25K-token cap); detail goes to `memory/topics/`. Save files AND commit before logging.
- Bash layer blocks `>` redirection, `rm -rf`, and `${VAR}` syntax — stage under `output/scratch/`, use plain `$VAR`.
- Root `notify`/`notify-jsonrender`/`secretcurl` are generated copies; untracked drift is harmless.
- Zero-token "completed" harness runs recur (09-22, 10-06) and self-heal; health issues #182/#184/#195/#196 stay open (skill-repair disabled).
- aeon-update: held new skills (no eyebrow binary); `dispatched` cron-state can stick after success — cross-check PR merge first.
- token-movers: GT and DS liquidity converged 09-30 (~$125-135K); mmETH pool is seeded, exclude from volume calcs.

## Active Targets
Detail: `memory/topics/priorities.md`.
- Hyperstitions: 1,000 stars (crossed 05-03), CN coverage, ≥3 integrators (14 as of 06-22) all resolved; @miroshark_ 1K followers unconfirmed.
- Stars: **1,475** (repo-pulse 10-21, +8 STEADY), forks 305. [source: logs/2026-10-21#repo-pulse]
- $MIROSHARK: ATH $0.0000436 (May 18); **$0.00000183 (-13.5% 24h, -8.0% 7d, -32.1% 30d), ~−96% from ATH, liq ~$107K** as of 2026-10-25, CONSOLIDATING; had rallied to $0.00000211 on 10-23-24 (RALLYING, +9.9% 7d). [source: logs/2026-10-25#token-movers]
- Team/treasury holdings: 12.37% of supply (2026-10-21), steady accumulation. [source: logs/2026-10-21#holdings]

## Next Priorities
- Next star threshold 1,500 (25 away at 1,475).
- `changelog` skill at 3 consecutive failures since 10-19 (1800s timeout, model glm-5.3-flash unrecognized); next run Mon 10-26 — check recovery. [source: logs/2026-10-23#heartbeat]
- aeon-update BLOCKED twice (10-21/22): classify script needs approval; baseline stuck at `3a747cd`, upstream now `f27af14` (~60 files). [source: logs/2026-10-21#aeon-update]
- Engine velocity: public repo's 6-window idle streak broke 10-12 (9 PRs, 7 substantive); watch if it persists. Website changelog PR miroshark-website#391 (draft).
- `products.md` gap: `x402aff-website` not listed under the Miroshark product repos (low urgency).
