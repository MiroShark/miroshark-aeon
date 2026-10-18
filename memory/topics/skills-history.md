---
type: Reference
name: skills-history
description: Archived skills rotated out of MEMORY.md Skills Built table
metadata:
  type: project
---

# Skills History Archive

| Skill | Date | Notes |
|-------|------|-------|
| surfaces ?type= filter | 2026-06-12 | PR #157 merged — server-side filter on /api/surfaces.json |
| feature validation fix | 2026-06-12 | self-improve PR #60 merged — feature skill runs tests in workspace, not /tmp |
| SECURITY.md | 2026-06-13 | PR #158 opened then closed (maintainer declined to merge) |
| CONTRIBUTING.md guide | 2026-06-14 | PR #162 — full dev setup + PR guide + zh-CN mirror |
| dependabot.yml | 2026-06-15 | PR #166 — 5-ecosystem dep scanning (pip/npm/docker/actions) |
| cost.json endpoint | 2026-06-16 | PR #179 — per-sim USD cost surface; lower bound with is_estimate + pricing_basis |
| tweet-digest prefetch | 2026-06-16 | PR #67 — adds tweet-digest case to prefetch-xai.sh |
| camel smoke test | 2026-06-17 | PR #183 — first agent-loop CI guard; fixes total_actions hardcoded 0 |
| cost on embed widget | 2026-06-19 | PR #190 — `~$X` cost pill on EmbedView |
| camel smoke test +content | 2026-06-20 | PR #196 — asserts real agent output (non-empty msgs+content) |
| graph_tools locale threading | 2026-06-21 | PR #198 — capture+use_locale across ThreadPoolExecutor in _fallback_interview |
| repo-actions Gate 3 (aeon) | 2026-06-20 | PR #69 — premise verification gate |
| repo-actions Gate 3 fix (aeon) | 2026-06-21 | PR #70 — unverifiable premise → drop/demote |
| thinking-token budget | 2026-06-22 | PR #203 CLOSED UNMERGED — LLM_REASONING_MAX_TOKENS/EFFORT |
| cost CLI subcommand | 2026-06-23 | PR #208 — `python cli.py cost <id>` |
| xai=quiet/skip split | 2026-06-24 | PR #75 |
| stop CLI subcommand | 2026-06-25 | PR #216 — cancel running sim |
| schedule tuning (aeon) | 2026-06-25 | PR #76 — pause build/content skills, stretch cadences |
