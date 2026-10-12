#!/usr/bin/env python3
import json, subprocess

UPSTREAM="aeonfun/aeon"; HEAD="df013dbe0be81e63771b7b013ec055380c766986"

def gh(a): return subprocess.run(["gh"]+a,capture_output=True,text=True,check=True).stdout
import os
head={t["path"]:t["sha"] for t in json.loads(gh(["api",f"repos/{UPSTREAM}/git/trees/{HEAD}?recursive=1"]))["tree"] if t["type"]=="blob"}

def git_blob_sha(path):
    if not os.path.exists(path): return None
    r=subprocess.run(["git","hash-object",path],capture_output=True,text=True)
    return r.stdout.strip() if r.returncode==0 else None

prior=json.load(open("memory/topics/aeon-update-state.json"))["pending_conflicts"]
prior_reason={e["path"]:e for e in prior}
staged=set(subprocess.run(["git","diff","--cached","--name-only"],capture_output=True,text=True,check=True).stdout.split())

thisrun={
 ".github/README.md":("fork MiroShark branding + skill-count table (82) vs upstream privacy/ecosystem refresh; 3-way overlap","df013db"),
 ".github/workflows/aeon.yml":("operator-customized workflow (env-narrow / model routing) vs upstream gateway/run-context + apt-get-hang fix + harness-snapshot wiring; 3-way overlap","d840d2f,e5e465d"),
 ".github/workflows/ci-tests.yml":("operator-customized (fork test list / env-narrow) vs upstream new test steps + biome check; 3-way overlap","fe7df9a"),
 "apps/cli/eslint.config.mjs":("modify/delete - fork removed the cli eslint config; upstream modified it. Held (keeps fork's deletion)","fe7df9a"),
 "apps/dashboard/package-lock.json":("coupled with apps/dashboard/package.json; lockfile 3-way conflict on the eslint/next bump","4b0ea879"),
 "apps/dashboard/package.json":("eslint/next version-bump held with its lock so npm ci stays consistent; 3-way conflict","4b0ea879"),
 "apps/webhook/eslint.config.mjs":("modify/delete - fork removed the webhook eslint config; upstream modified it. Held (keeps fork's deletion)","fe7df9a"),
 "docs/examples/README.md":("fork skill-count (82) vs upstream count refresh; 3-way overlap. Held with the README skill-count cluster","df013db"),
 "llms.txt":("fork-only MiroShark copy vs upstream refresh; 3-way overlap","df013db"),
 ".github/workflows/ci-skill-packs.yml":("operator-customized workflow (env-narrow) vs upstream; 3-way overlap (prior 'coupled validator' note now stale - the validator itself is synced)","914dfe17"),
}

paths=set(prior_reason)|set(thisrun)
kept=[]
for p in sorted(paths):
    if p in staged: continue
    hs=head.get(p); ls=git_blob_sha(p)
    if hs is None:
        if p in prior_reason and "enabled-skill-removed" in prior_reason[p].get("reason",""):
            kept.append(prior_reason[p])
        continue
    if ls==hs: continue
    if p in thisrun:
        kept.append({"path":p,"reason":thisrun[p][0],"upstream_commits":thisrun[p][1].split(",")})
    else:
        e=prior_reason[p]
        kept.append({"path":e["path"],"reason":e["reason"],"upstream_commits":e.get("upstream_commits",[])})

# applied counts from staged
ns=subprocess.run(["git","diff","--cached","--name-status"],capture_output=True,text=True,check=True).stdout.splitlines()
added=sum(1 for l in ns if l.startswith("A"))
deleted=sum(1 for l in ns if l.startswith("D"))
modified=sum(1 for l in ns if l.startswith("M"))

state={
 "baseline_sha":HEAD,
 "upstream":UPSTREAM,
 "last_run":"2026-10-12",
 "last_pr":None,
 "applied":{"added":added,"updated":modified,"deleted":deleted},
 "pending_conflicts":kept,
}
with open("memory/topics/aeon-update-state.json","w") as fh:
    json.dump(state,fh,indent=2)
    fh.write("\n")
print(f"wrote state: applied add={added} upd={modified} del={deleted}; pending={len(kept)}")
