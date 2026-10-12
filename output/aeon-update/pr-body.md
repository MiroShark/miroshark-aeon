## Upstream sync: `aeonfun/aeon` `1a7f07e..df013db`

**27 commits** (2026-10-05 → 2026-10-10) · **183 applied** · **22 manual** · baseline → `df013db`.

Pulled by `aeon-update`. Operator-owned paths (`aeon.yml`, `soul/`, `memory/`, `STRATEGY.md`, `.mcp.json`) are never written — surfaced below. The baseline SHA is committed in this branch, so merging advances the watermark; the 22 conflicts are tracked in `memory/topics/aeon-update-state.json` and resurface each run until reconciled.

### Applied cleanly
- **New files:** `biome.json` _(repo-wide Biome formatter config, #1193)_
- **Removed (upstream dropped):** `plugin/.minimax-plugin/plugin.json`, `plugin/plugin.json` _(MiniMax + agent-plugins manifests retired, #1182 #1187)_
- **Modified skills:** `aeon-update`, `create-skill`, `skill-repair` _(haiku tier → `claude-haiku-5-5` #1189, tightened secrets guidance #1179, mine-history plugin-root fallback #1183 — body-only, no frontmatter change so catalogs unchanged)_
- **Setup/dev skill:** `.claude/skills/aeon/**` + `plugin/skills/aeon/**` _(refreshed references: ci triggers, history-mining, layout, mcp, secrets, skill-anatomy)_
- **Apps:** `apps/cli/**`, `apps/dashboard/**`, `apps/mcp-server/**`, `apps/webhook/**` _(Biome reformat across all apps #1193; mcp-server resolved-model + 1800s timeout + hosted-MCP pointers #1190 #1191 #1192; dashboard lib/components/api sweep)_
- **Scripts / harness:** `scripts/llm-gateway.sh` _(3-way merged)_, `scripts/fleet-scorecard.mjs`, `scripts/notify-jsonrender.sh`, `scripts/tests/*`, `bin/add-mcp`
- **Workflows:** `.github/workflows/ci-apps.yml` _(3-way merged: ubuntu-24.04 pin + harness-cli wiring)_, `.github/workflows/ci-harness-cli.yml`
- **Catalog:** `catalog/skill-packs.json` + `docs/community-skill-packs.md` _(Epoch Pack #1168, bon travail Pack #1167 — validator OK, 11 packs)_
- **Docs / other:** `docs/aeon-setup.md` _(3-way merged — fork's 82 skill-count preserved, upstream prose applied)_, `docs/CONFIGURATION.md`, `docs/ECOSYSTEM.md`, `docs/ADK.md`, `docs/mcp-oauth.md`, `CHANGELOG.md`, `package.json`, `.github/CONTRIBUTING.md`, `.github/SECURITY.md`, plugin manifests

**Auto-merged (3-way — your local customization kept, upstream's disjoint changes applied):** `.github/workflows/ci-apps.yml`, `docs/aeon-setup.md`, `scripts/llm-gateway.sh`. Review these merged hunks.

CI pre-checks run against the branch: `validate-skill-packs` OK (11 packs), `validate-readme-catalog` OK (82 skills consistent across README / docs / hero), `validate-config aeon.yml` CLEAN (71 skills resolve). eyebrow: the 3 edited skills' lock entries already match upstream HEAD (no new skills), so `ci-skill-integrity` stays green.

### Needs manual review (22 conflicts — your local copy diverges from upstream)

**Skill-count cluster (fork is internally consistent at 82; upstream moved to 85).** Reconcile as one edit if you want to adopt upstream's count:
- `.github/README.md` — fork MiroShark branding + 82-skill table vs upstream privacy/ecosystem refresh.
- `docs/examples/README.md` — upstream bumped the count to 85 and added hosted-MCP copy; fork holds 82. Upstream diff:
  ```diff
  -...call its 85 skills. The scripts here are the shortest possible "first call works" demos...
  +...call its 85 skills. ...Using ChatGPT or Cursor...? The hosted server at www.aeon.fun/connect/mcp...
  ```
- `docs/skill-packs.md`, `docs/assets/hero-animated.svg` — carry the 85 count; held with the cluster.
- `llms.txt` — fork-only MiroShark copy vs upstream hosted-MCP-server additions.

**Workflows (fork env-narrow / model routing vs upstream changes):**
- `.github/workflows/aeon.yml` — vs upstream gateway/run-context + apt-get-hang fix + harness-adapter-snapshot wiring (#1180 #1186).
- `.github/workflows/ci-tests.yml` — vs upstream apt-get-hang hardening + biome check (#1186 #1193). Upstream diff:
  ```diff
  -APT_OPTS="-o DPkg::Lock::Timeout=120"
  -sudo apt-get $APT_OPTS update -qq && sudo apt-get $APT_OPTS install -y -qq bubblewrap
  +APT_OPTS="...Acquire::Retries=3 -o Acquire::http::Timeout=20..."
  +if ! command -v bwrap ...; then ... sudo timeout 90 apt-get $APT_OPTS update ...; fi
  ```
- `.github/workflows/ci-skill-packs.yml` — fork env-narrow vs upstream (prior "coupled validator" note is stale — the validator itself is now synced).

**Dependency bumps held as package.json + lockfile units (apply both together or neither, else `npm ci` breaks):**
- `apps/dashboard/package.json` + `apps/dashboard/package-lock.json` — eslint 10 / next 16 bump (#1171-#1173).
- `apps/webhook/package.json` + `apps/webhook/package-lock.json` — wrangler bump (#1174-#1175, carried).

**modify/delete (fork removed the file, upstream modified it — held to respect your deletion):**
- `apps/cli/eslint.config.mjs`, `apps/webhook/eslint.config.mjs`, `apps/dashboard/eslint.config.mjs`.

**Customized skills (fork edits vs upstream prose update):**
- `skills/fetch-tweets/SKILL.md`, `skills/shiplog/SKILL.md` — vs upstream xai/grok/coingecko refresh (#9cb0b6a9, carried).

**Not adopted (would shift the skill count / membership the held docs depend on):**
- `skills/feedback-builder/SKILL.md` — new upstream skill; adopt manually (fetch SKILL.md, bump README/docs counts, eyebrow scan + regen catalogs).
- `skills/compute-resell/SKILL.md` + `config.example.json` — fork removed it; upstream modified it.

**Binary:**
- `docs/assets/proof-aeon.jpg` — fork image vs upstream refresh; cannot 3-way merge.

### Operator config changed upstream (not auto-applied — reconcile by hand)
- `aeon.yml` — upstream touched it (run-context / defaults). Your enable/schedule/model choices are untouched here; merge any new skill entries you want by hand.

### Upstream commits
| SHA | Summary |
|-----|---------|
| 81c53c1 | docs(packs): list the Epoch Pack (#1168) |
| 09a6697 | docs(packs): list the bon travail Pack (#1167) |
| e2aae65 | fix(ci): drop restore-keys on Claude Code npm cache (#1169) |
| 4614846 | plugin: fit Codex manifest to OpenAI directory limits (#1176) |
| 67a8150 | plugin: fix OpenAI directory metadata findings (#1178) |
| 38f6ab8 | fix(skills): catch stateless ghs_ tokens in the secret tripwire (#1177) |
| f252074 | aeon skill: tighten secrets-handling guidance (#1179) |
| 595fa40 | chore(deps): bump source-map-js (dashboard) (#1171) |
| 768650a | chore(deps): bump proxy-addr (mcp-server) (#1174) |
| 00761e9 | chore(deps): bump @modelcontextprotocol/sdk (mcp-server) (#1175) |
| bd0fbc6 | chore(deps): bump npm_and_yarn group, 3 updates (#1173) |
| b591603 | chore(deps): bump sharp (dashboard) (#1172) |
| d840d2f | fix(ci): run the harness from a snapshot (#1180) |
| 6ec6f28 | chore(plugin): drop the MiniMax manifest (#1182) |
| 1375769 | chore(plugin): fill the Claude directory listing fields (#1184) |
| 9407d70 | aeon skill: plugin-root fallback for mine-history, drop pr-check (#1183) |
| e67afe8 | docs(aeon skill): refresh ci-tests triggers + new-skill gate count (#1185) |
| e5e465d | fix(workflow): stop apt-get update hangs killing read-only runs (#1186) |
| 5f41362 | chore(plugin): drop the agent-plugins manifest (#1187) |
| 9ecb3c3 | chore(plugin): shorter Claude directory description (#1188) |
| 11aa692 | chore(models): move the haiku tier to Claude Haiku 5.5 (#1189) |
| e20445b | fix(mcp-server): drop undefined cron, tier run notes, 1800s timeout (#1190) |
| b6233ee | fix(mcp-server): pass resolved model to run-harness (#1191) |
| 1560dcc | docs: point to hosted MCP server at www.aeon.fun/connect/mcp (#1192) |
| fe7df9a | chore(apps): add Biome formatter + format check for all apps (#1193) |
| c0cb7c4 | aeon-update: treat .github/dependabot.yml as operator-owned (#1194) |
| df013db | docs(ecosystem): fix dead avatars, renamed handles, epoch pack repo (#1196) |

🤖 Generated with [Claude Code](https://claude.com/claude-code)
