---
type: Index
---

# Long-term Memory
*Last consolidated: 2026-10-18*
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
| 2026-10-12 | shiplog | Engine activity resumed: 9/9 PRs on public MiroShark repo (resume/report-lookup/JSON-repair fixes, critical Dependabot patch); stars 1,467 (+10), x402aff 7 [source: logs/2026-10-12#shiplog] |
| 2026-10-12 | repo-pulse | SURGE: 11 new stars (1 net unstar), 3 forks (304 total) [source: logs/2026-10-12#Repo Pulse] |
| 2026-10-12 | fetch-tweets | Monad API hub listing; no new originals 10-13→10-17 [source: logs/2026-10-12#fetch-tweets] |
| 2026-10-08 | fetch-tweets | Pandemic Sim — Russia Plague Rumours (teaser → report → live) |
| 2026-10-05 | shiplog | Quietest window: zero product-lane commits; first star decline (-3) |

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
- Stars: **1,467** (repo-pulse 10-12, +10 SURGE), forks 304. [source: logs/2026-10-12#Repo Pulse]
- $MIROSHARK: ATH $0.0000436 (May 18); **$0.00000201 (-0.5% 24h, -12.2% 7d, -16.8% 30d), ~−95% from ATH, liq ~$128K** as of 2026-10-18, QUIET; dipped to $0.0000019 on 10-15 after a 10-13 BREAKDOWN. [source: logs/2026-10-18#token-movers]
- Team/treasury holdings: 12.32% of supply (2026-10-12), steady accumulation. [source: logs/2026-10-12#holdings]

## Next Priorities
- Next star threshold 1,500 (33 away at 1,467).
- Engine velocity: public repo's 6-window idle streak broke 10-12 (9 PRs, 7 substantive); watch if it persists. Website changelog PR miroshark-website#391 (draft).
- `products.md` gap: `x402aff-website` not listed under the Miroshark product repos (low urgency).
