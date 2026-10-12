#!/usr/bin/env python3
import json, subprocess, re, os, base64, tempfile, sys

UPSTREAM = "aeonfun/aeon"
BASE = "1a7f07e1b259eb46abb472139bb3284d64beee54"
HEAD = "df013dbe0be81e63771b7b013ec055380c766986"
WORK = "output/aeon-update/work"
os.makedirs(WORK, exist_ok=True)

def gh(args):
    return subprocess.run(["gh"] + args, capture_output=True, text=True, check=True).stdout

def tree(ref):
    data = json.loads(gh(["api", f"repos/{UPSTREAM}/git/trees/{ref}?recursive=1"]))
    return {t["path"]: t["sha"] for t in data["tree"] if t["type"] == "blob"}

head = tree(HEAD)
base = tree(BASE)

loc = {}
for line in subprocess.run(["git","ls-files","-s"],capture_output=True,text=True,check=True).stdout.splitlines():
    m = re.match(r"^\S+ (\S+) \S+\t(.*)$", line)
    if m: loc[m.group(2)] = m.group(1)

cmp = json.loads(gh(["api", f"repos/{UPSTREAM}/compare/{BASE}...{HEAD}"]))

_blobcache = {}
def blob(sha):
    if sha in _blobcache: return _blobcache[sha]
    data = json.loads(gh(["api", f"repos/{UPSTREAM}/git/blobs/{sha}"]))
    content = base64.b64decode(data["content"]) if data.get("encoding")=="base64" else data["content"].encode()
    _blobcache[sha] = content
    return content

def is_operator(f):
    if f in ("aeon.yml","STRATEGY.md",".mcp.json","aeon.db","skills.lock","eyebrowlock.json"): return True
    for p in ("soul/","memory/","output/","apps/dashboard/outputs/"):
        if f.startswith(p): return True
    if f.startswith(".env"): return True
    if f.startswith(".claude/") and not f.startswith(".claude/skills/aeon/"): return True
    if re.match(r"^catalog/.*\.json$", f) and f != "catalog/skill-packs.json": return True
    return False

def write_file(path, content):
    d = os.path.dirname(path)
    if d: os.makedirs(d, exist_ok=True)
    with open(path, "wb") as fh: fh.write(content)

def parse_ok(path):
    try:
        if path.endswith(".json"):
            with open(path) as fh: json.load(fh)
        elif path.endswith((".yml",".yaml")):
            import yaml  # may not be available
            with open(path) as fh: yaml.safe_load(fh)
    except ImportError:
        return True  # cannot check yaml, assume ok
    except Exception as e:
        return False
    return True

res = {"clean_update":[], "clean_add":[], "clean_delete":[], "clean_merge":[],
       "conflict":[], "operator":[], "skip":[], "unreadable":[]}

for fo in cmp["files"]:
    st = fo["status"]; f = fo["filename"]; pf = fo.get("previous_filename")
    try:
        if is_operator(f):
            res["operator"].append({"f":f,"st":st}); continue
        if st == "modified":
            if loc.get(f) == head.get(f):
                res["skip"].append(f)
            elif loc.get(f) == base.get(f):
                write_file(f, blob(head[f]))
                if not parse_ok(f):
                    res["conflict"].append({"f":f,"reason":"clean-update-parse-fail"})
                else:
                    res["clean_update"].append(f)
            elif f not in loc or not os.path.exists(f):
                # modify/delete: upstream modified a file the fork removed. Hold.
                res["conflict"].append({"f":f,"reason":"modify-delete-fork-removed"})
            else:
                # 3-way merge
                lp = os.path.join(WORK,"local"); bp = os.path.join(WORK,"base"); hp = os.path.join(WORK,"head")
                with open(lp,"wb") as fh: fh.write(open(f,"rb").read())
                with open(bp,"wb") as fh: fh.write(blob(base[f]) if f in base else b"")
                with open(hp,"wb") as fh: fh.write(blob(head[f]))
                r = subprocess.run(["git","merge-file","-p","--diff3",lp,bp,hp],capture_output=True)
                if r.returncode == 0:
                    write_file(f, r.stdout)
                    if not parse_ok(f):
                        # revert to local original from index
                        subprocess.run(["git","checkout","--","{}".format(f)])
                        res["conflict"].append({"f":f,"reason":"merge-parse-fail","commits":fo.get("commits")})
                    else:
                        res["clean_merge"].append(f)
                else:
                    res["conflict"].append({"f":f,"reason":"3way-overlap"})
        elif st == "added":
            if f in loc:
                if loc.get(f) == head.get(f):
                    res["skip"].append(f)
                else:
                    res["conflict"].append({"f":f,"reason":"add-collision"})
            else:
                write_file(f, blob(head[f]))
                if not parse_ok(f):
                    os.remove(f); res["conflict"].append({"f":f,"reason":"clean-add-parse-fail"})
                else:
                    res["clean_add"].append(f)
        elif st == "removed":
            if f not in loc:
                res["skip"].append(f)
            elif loc.get(f) == base.get(f):
                if os.path.exists(f): os.remove(f)
                res["clean_delete"].append(f)
            else:
                res["conflict"].append({"f":f,"reason":"del-conflict-local-diverged"})
        elif st == "renamed":
            res["conflict"].append({"f":f,"reason":f"renamed-from-{pf}-manual"})
        else:
            res["conflict"].append({"f":f,"reason":f"unhandled-{st}"})
    except subprocess.CalledProcessError as e:
        res["unreadable"].append({"f":f,"err":str(e)})

print(json.dumps(res, indent=2))
summary = {k:len(v) for k,v in res.items()}
print("SUMMARY", json.dumps(summary), file=sys.stderr)
