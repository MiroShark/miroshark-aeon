#!/usr/bin/env python3
import json, subprocess, re, sys

UPSTREAM = "aeonfun/aeon"
BASE = "1a7f07e1b259eb46abb472139bb3284d64beee54"
HEAD = "df013dbe0be81e63771b7b013ec055380c766986"

def gh(args):
    return subprocess.run(["gh"] + args, capture_output=True, text=True, check=True).stdout

def tree(ref):
    out = gh(["api", f"repos/{UPSTREAM}/git/trees/{ref}?recursive=1"])
    data = json.loads(out)
    return {t["path"]: t["sha"] for t in data["tree"] if t["type"] == "blob"}

head = tree(HEAD)
base = tree(BASE)

# local index blob shas
loc = {}
out = subprocess.run(["git", "ls-files", "-s"], capture_output=True, text=True, check=True).stdout
for line in out.splitlines():
    # mode sha stage\tpath
    m = re.match(r"^\S+ (\S+) \S+\t(.*)$", line)
    if m:
        loc[m.group(2)] = m.group(1)

# compare files
cmp = json.loads(gh(["api", f"repos/{UPSTREAM}/compare/{BASE}...{HEAD}"]))
files = cmp["files"]

def is_operator(f):
    if f in ("aeon.yml","STRATEGY.md",".mcp.json","aeon.db","skills.lock","eyebrowlock.json"):
        return True
    for p in ("soul/","memory/","output/","apps/dashboard/outputs/"):
        if f.startswith(p):
            return True
    if f.startswith(".env"):
        return True
    if f.startswith(".claude/") and not f.startswith(".claude/skills/aeon/"):
        return True
    if re.match(r"^catalog/.*\.json$", f) and f != "catalog/skill-packs.json":
        return True
    return False

rows = []
for fo in files:
    st = fo["status"]
    f = fo["filename"]
    pf = fo.get("previous_filename")
    if is_operator(f):
        rows.append(("OPERATOR", st, f))
        continue
    if st == "modified":
        if loc.get(f) == head.get(f):
            rows.append(("SKIP", st, f))
        elif loc.get(f) == base.get(f):
            rows.append(("CLEAN-UPDATE", st, f))
        else:
            rows.append(("3WAY", st, f))
    elif st == "added":
        if f in loc:
            rows.append(("ADD-COLLIDE", st, f))
        else:
            rows.append(("CLEAN-ADD", st, f))
    elif st == "removed":
        if f not in loc:
            rows.append(("SKIP-GONE", st, f))
        elif loc.get(f) == base.get(f):
            rows.append(("CLEAN-DELETE", st, f))
        else:
            rows.append(("DEL-CONFLICT", st, f))
    elif st == "renamed":
        info = f"prev={pf} locprev={pf in loc} locnew={f in loc} loc_eq_baseprev={loc.get(pf)==base.get(pf)} locnew_eq_head={loc.get(f)==head.get(f)}"
        rows.append(("RENAME", st, f + " | " + info))
    else:
        rows.append(("OTHER", st, f))

rows.sort()
for d, st, f in rows:
    print(f"{d}\t{st}\t{f}")

# summary counts
from collections import Counter
c = Counter(r[0] for r in rows)
print("=== COUNTS ===", dict(c), file=sys.stderr)
