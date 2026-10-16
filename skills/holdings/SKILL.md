---
name: holdings
description: Report your wallet holdings of the instance's token - amount held, % of total supply, and 7d/30d amount growth, via public RPC (no dollar value)
metadata:
  title: Holdings
  category: crypto
  var: ""
  tags:
    - crypto
  mode: write
  requires:
    - BASE_RPC_URL?
    - SOLANA_RPC_URL?
  capabilities:
    - external_api
---

> **${var}** — Optional single wallet address to check (Base `0x…` or Solana). If empty, uses every wallet in `memory/holdings.json`.

## What this does

Reads a set of your wallets and the project tokens to track, then reports, per token:

- **Amount held**.
- **% of total supply** you hold (`amount ÷ total_supply`).
- **7d and 30d holdings growth** — the change in your **token amount** over the
  window (did you accumulate or sell).

**No dollar value / price is reported** — this is a holdings tracker, not a
portfolio-value report. Amounts and supply share only.

On-chain balances come from **public, keyless RPC** (`https://mainnet.base.org` for
Base, `https://api.mainnet-beta.solana.com` for Solana); total supply comes from
GeckoTerminal. No API key required — override the RPC with `BASE_RPC_URL` /
`SOLANA_RPC_URL` if you have an authenticated node.

Each instance tracks **its own token**: this config holds one token — aeon on the
aeon instance, MiroShark on the MiroShark instance. Add a second `tokens` entry only
if an instance should report both.

**Growth = amount, not price.** 7d/30d growth is the change in how many tokens you
hold, measured against this skill's own prior snapshots (`HOLDINGS_STATE:` lines in
`memory/logs`). There is no price-history fetch — the skill builds its own history,
one snapshot per run. On the first runs the 7d/30d fields are simply absent (no
snapshot that far back yet) and fill in as the log accumulates: once a snapshot
~7 days back exists the 7d figure appears, ~30 days back the 30d figure. This skill
runs weekly, so 7d lands on the second run and 30d after ~4-5 runs.

Note: on-chain `totalSupply()` reverts on the DERC20 aeon contract, so total supply
comes from GeckoTerminal (`total_supply`, 100,000,000,000 aeon).

## Config

Reads `memory/holdings.json`:

```json
{
  "wallets": [
    {"address": "0x…", "label": "personal", "chain": "base"},
    {"address": "8mjM…", "label": "sol", "chain": "solana"}
  ],
  "tokens": [
    {"symbol": "aeon", "contract": "0xbf8e8f0e8866a7052f948c16508644347c57aba3", "chain": "base", "decimals": 18}
  ]
}
```

A token is checked against every wallet on the **same chain**. Add the miroshark
token as a second `tokens` entry once its contract is known.

If `${var}` is set, check only that one address (chain inferred: `0x`-prefixed →
base, else solana) against every token on that chain, ignoring the wallet list.

If `memory/holdings.json` is missing **and** `${var}` is empty, abort silently — no
notification, no article.

## Steps

### 1. Fetch balances + prices

```bash
python3 skills/holdings/holdings.py memory/holdings.json
```

The helper (Python stdlib only, sandbox-safe) prints JSON:

- `rows[]` — one per (token, wallet): `symbol`, `chain`, `wallet`, `label`,
  `amount` (or `error` if a fetch failed).
- `per_symbol` — totals per token: `amount`, `total_supply`, `pct_supply` (% of
  supply held).
- `growth` - per token, the change vs prior snapshots for `last` (newest prior
  snapshot), `7d` and `30d`: each `{date, gap_days, amount_then, amount_delta,
  amount_delta_pct}` or `null` when no snapshot falls in the window (see step 2).

`pct_supply` may be `null` if GeckoTerminal lacked supply for that token — render
`n/a`, do not abort. The helper reads the prior snapshots itself (`HOLDINGS_STATE:`
lines in `memory/logs`). No dollar value is produced.

If `${var}` is set, check that one wallet against this instance's own tokens (read
from `memory/holdings.json`) — only the wallet is overridden, the token list stays
instance-specific:

```bash
ADDR="${var}"
CHAIN=base; [ "${ADDR#0x}" = "$ADDR" ] && CHAIN=solana
python3 - "$ADDR" "$CHAIN" > /tmp/holdings-var.json <<'PY'
import json,sys
addr,chain=sys.argv[1],sys.argv[2]
cfg=json.load(open("memory/holdings.json"))
json.dump({"wallets":[{"address":addr,"label":"var","chain":chain}],
           "tokens":[t for t in cfg["tokens"] if t["chain"]==chain]},sys.stdout)
PY
python3 skills/holdings/holdings.py /tmp/holdings-var.json --no-history
```

A single `${var}` wallet has no snapshot series, so `--no-history` drops `growth`;
leave the 7d/30d columns out of that report.

If a row has `"error"`, retry `holdings.py` once. If it still errors on the RPC
(sandbox block / 403 / timeout), note `rpc=fetch_fail` in the footer for that wallet
and continue — a partial report still beats nothing. If `pct_supply` is `null`
(GeckoTerminal supply miss), report the raw amount and mark `% Supply` as `n/a`, do not
abort.

### 2. Read holdings growth from the helper

`holdings.py` already picked the windows from the `HOLDINGS_STATE:` lines (written in
step 4) in `memory/logs` and `memory/logs/archive`. Do not recompute them; render
`growth.<symbol>`:

- **7d** - the snapshot closest to 7 days ago, within +/-2 days.
- **30d** - the snapshot closest to 30 days ago, within +/-4 days.
- **last** - the newest prior snapshot at any age (used by the step 5 skip rule).

Each window carries `amount_delta` (tokens; + = accumulated, - = sold),
`amount_delta_pct` and `date` / `gap_days` of the snapshot it compares against.
Report growth as tokens and percent, e.g. `7d +1.20B (+10.3%)` or `30d +0` (flat).
This is holdings movement only, it does not move with price.

A `null` window (no snapshot in range, e.g. early runs or an off-schedule run) renders
as `building`: never print `+0` for "no data", and never fall back to a snapshot
outside the range. `+0` is reserved for a window that HAS a snapshot and the amount
genuinely did not change. `growth.<symbol>.partial = true` means a wallet fetch
failed, so the total is partial: show the windows as `n/a` for that token.

If `growth` is missing (the helper failed before it), leave the growth columns blank
and say so in the footer. Never do the window math by hand.

### 3. Compile the report

Save to `output/articles/holdings-${today}.md`:

```markdown
# Holdings — ${today}

| Token | Amount | % Supply | 7d | 30d |
|-------|--------|----------|-----|-----|
| aeon  | 12.82B | 12.82% | +1.20B (+10.3%) | +2.10B (+19.6%) |

7d/30d are the change in token **amount** held over the window (accumulation/sell),
from prior snapshots. A window with no snapshot yet is blank (`building`), not `0`.
`+0` means a real no-change.

## By wallet
| Wallet | Amount |
|--------|--------|
| aeon-safe (0xf1e9…158e) | 12.53B |
| aeon-deployer (0x6797…e3a2) | 285.32M |

---
*Balances: public RPC (base=mainnet.base.org). Supply: GeckoTerminal. Growth: own snapshots.*
*Sources: rpc=[ok|fetch_fail] · supply=[ok|na] · growth=[Nd history|building]*
```

Format large token counts compactly (`12.82B`, `285.3M`, `1.20K`), `% Supply` to two
decimals. Omit the "By wallet" table if there is only one wallet (it duplicates the
top table).

### 4. State log (powers tomorrow's deltas)

Append to `memory/logs/${today}.md`:

```
### holdings
- HOLDINGS_STATE: date=${today} aeon_amount=XXXX.XX aeon_pct_supply=XX.XX
- Article: output/articles/holdings-${today}.md
- Sources: rpc=ok supply=ok
```

The `HOLDINGS_STATE:` line is the snapshot store — this is the "history it builds at
each run". Step 2 of every future run parses it with a key=value split. Include a
`date=` field plus, per tracked token, `<symbol>_amount` + `<symbol>_pct_supply` (no
dollar fields). No thousands separators, full-precision `_amount` (do not pre-round —
the 7d/30d deltas subtract these). Keep key order stable. Always write this line,
even on a flat/quiet run, so the series stays unbroken (a missing day just widens the
nearest-snapshot search window).

### 5. Notify

```
*Holdings — aeon*

12.82B · 12.82% of supply
7d +1.20B (+10.3%) · 30d +2.10B (+19.6%)
_Balances: public RPC. Supply: GeckoTerminal. Growth: own snapshots (7d vs 2026-10-05). ${today}_
```

The title names the tracked token. The growth line shows token-amount change over
the window; render `building` for a window with no snapshot yet, `+0` for a real
no-change. With more than one tracked token, repeat the two-line block per token.
End with the one-line sources footer (where each number came from, the snapshot
date the 7d figure compares against, the run date); drop the 7d date when 7d is
`building`.

**Skip rule:** if no token's amount changed since the last run
(`growth.<symbol>.last.amount_delta` is 0 for every token), send a single line
`aeon holdings flat — 12.82B (12.82% of supply).` instead of the full block. On a
total RPC failure (every wallet `fetch_fail`), log only — no notification.

## Sandbox note

`holdings.py` uses only the Python stdlib and sends a browser `User-Agent` (the
public `mainnet.base.org` endpoint 403s the default urllib UA). All reads are public
and keyless; no `secretcurl`, no secrets. If the sandbox blocks the RPC POST, the
row carries an `error` and the skill degrades to a partial report — it never invents
a balance.

## Constraints

- Never invent a balance or price. Every number traces to an RPC response or a
  GeckoTerminal price. A failed fetch is reported as `fetch_fail`, not zero.
- A zero balance (wallet holds none of the token) is real data — report `0`, distinct
  from `fetch_fail`.
- Preserve the `HOLDINGS_STATE:` log schema — tomorrow's deltas depend on it.
- Public RPC only by default; only use `BASE_RPC_URL`/`SOLANA_RPC_URL` overrides, and
  put any key in the URL path, never a header (sandbox blocks env expansion in `-H`).
