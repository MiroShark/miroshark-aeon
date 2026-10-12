**aeon-update — 2026-10-12**
synced 27 upstream commits → PR #204

`aeonfun/aeon` `1a7f07e..df013db`. 183 files applied clean, 22 held for manual review. Baseline → `df013db` (advances on merge).

**Applied:** Biome across all apps + new `biome.json`; haiku tier → `claude-haiku-5-5`; mcp-server resolved-model / 1800s / hosted-MCP pointers; Epoch + bon travail packs. 3 clean 3-way merges (`ci-apps.yml`, `docs/aeon-setup.md` kept the fork's 82 count, `scripts/llm-gateway.sh`). CI pre-checks green: skill-packs, readme-catalog (82), config.

**Manual (22):** skill-count cluster (fork 82 vs upstream 85 — README / examples / llms.txt), fork workflows (`aeon.yml` / `ci-tests.yml`), dashboard + webhook dep bumps (held with their locks), 3 fork-deleted eslint configs, `fetch-tweets` / `shiplog` edits, not-adopted `feedback-builder` / `compute-resell`.

PR: https://github.com/aaronjmars/miroshark-aeon/pull/204
