#!/usr/bin/env bash
# Consolidate the OpenAI baseline: nano full suite + event-driven-bus re-run (mini/5.5),
# spliced into baselines/openai-gpt5/results.json with metrics/manifest/report.
# Run from the repo root with OPENAI_API_KEY already exported in your shell:
#     bash consolidate_openai.sh
# Stops immediately if any run returns API-error rows (no fabricated numbers).
set -euo pipefail

python3 run_evals.py --validate-cases >/dev/null && echo "cases OK"

err_check() {  # stop if the last run produced API error rows
  python3 - "$1" <<'PY'
import json,sys
d=json.load(open("results/results.json")); rows=d["results"] if isinstance(d,dict) else d
errs=[r for r in rows if r.get("source")=="error" or "error" in r]
if errs:
    print(f"[{sys.argv[1]}] {len(errs)} API ERROR rows — STOPPING:", str(errs[0].get('error',''))[:160]); sys.exit(1)
print(f"[{sys.argv[1]}] ok — {len(rows)} rows, no API errors")
PY
}

echo "== Step 1: gpt-5.4-nano, full suite =="
python3 run_evals.py --runner openai --model gpt-5.4-nano --samples 5 --fix-rounds 2 --variants with,without
err_check nano; cp results/results.json baselines/openai-gpt5/results-nano.json

echo "== Step 2: event-driven-bus, mini + 5.5 =="
python3 run_evals.py --runner openai --models gpt-5.4-mini,gpt-5.5 --samples 5 --fix-rounds 2 --variants with,without --only event-driven-bus
err_check edb; cp results/results.json baselines/openai-gpt5/results-edb-mini55.json

echo "== Step 3: splice (offline, asserted) =="
python3 - <<'PY'
import json
def rows_of(p):
    d=json.load(open(p)); return d if isinstance(d,list) else next(v for v in d.values() if isinstance(v,list))
B="baselines/openai-gpt5/"
mini55=rows_of(B+"results-mini55.json"); edb=rows_of(B+"results-edb-mini55.json"); nano=rows_of(B+"results-nano.json")
keep=[r for r in mini55 if r["model"] in {"gpt-5.4-mini","gpt-5.5"} and r["case_id"]!="event-driven-bus"]
out=keep+edb+nano
models=sorted(set(r["model"] for r in out))
assert models==["gpt-5.4-mini","gpt-5.4-nano","gpt-5.5"], models
for m in models:
    for v in ("with","without"):
        cs=set(r["case_id"] for r in out if r["model"]==m and r["variant"]==v)
        assert len(cs)==54, (m,v,len(cs)); assert "event-driven-bus" in cs, (m,v)
k=[(r["model"],r["case_id"],r["variant"],r["sample"]) for r in out]
assert len(k)==len(set(k)), "duplicate (model,case,variant,sample) rows"
json.dump({"results":out}, open(B+"results.json","w"))
print(f"spliced {len(out)} rows; models={models}; asserts OK")
PY

echo "== Step 4: metrics + MANIFEST + REPORT =="
python3 harness/quality.py --dump-metrics results/raw baselines/openai-gpt5/results.json > baselines/openai-gpt5/baseline-metrics.json
cat > baselines/openai-gpt5/MANIFEST.txt <<EOF
version: openai-gpt5
generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)
models: gpt-5.4-nano, gpt-5.4-mini, gpt-5.5
samples: 5  fix_rounds: 2
skill_fingerprint: sha256:c3f30e363f88
provenance: surgical consolidation — nano full suite + event-driven-bus re-run folded into the
  prior mini/5.5 snapshot; gpt-5.5-pro excluded (Responses-API-only). Intermediates kept:
  results-nano.json, results-edb-mini55.json, results-mini55.json.
EOF
python3 - <<'PY'
import json,tempfile,shutil,os,sys; sys.path.insert(0,".")
from harness.report import render
from harness.cases import load_cases
rows=json.load(open("baselines/openai-gpt5/results.json"))["results"]
prov={"models":"gpt-5.4-nano, gpt-5.4-mini, gpt-5.5","runner":"openai","temperature":0.0,
      "samples":5,"fix_rounds":2,"skill_fingerprint":"sha256:c3f30e363f88 (content)"}
t=tempfile.mkdtemp(); render(rows, load_cases("cases"), t, provenance=prov)
for f in os.listdir(t):
    if f.startswith("REPORT"): shutil.copy(os.path.join(t,f), "baselines/openai-gpt5/"+f)
shutil.rmtree(t,ignore_errors=True); print("REPORT regenerated")
PY

echo "== per-model table (pass@1 over 54 cases) =="
python3 - <<'PY'
import json,collections
rows=json.load(open("baselines/openai-gpt5/results.json"))["results"]
by=collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
for r in rows: by[r["model"]][r["case_id"]][r["variant"]].append(bool(r["passed"]))
print(f"{'model':<14}{'with':>8}{'without':>9}{'lift':>8}{'corrective':>12}{'regress':>9}")
for m in sorted(by):
    cw=[];co=[];fixn=off=reg=0
    for c,cv in by[m].items():
        w=cv.get("with");o=cv.get("without")
        if not w or not o: continue
        rw=sum(w)/len(w);ro=sum(o)/len(o);cw.append(rw);co.append(ro)
        if ro<0.5: off+=1; fixn+= rw>=0.5
        if ro>=0.5 and rw<0.5: reg+=1
    pw=sum(cw)/len(cw)*100;po=sum(co)/len(co)*100
    print(f"{m:<14}{pw:>7.1f}%{po:>8.1f}%{pw-po:>+7.1f}{f'{fixn}/{off}':>12}{reg:>9}")
PY
echo; echo "DONE — tell Claude 'done' to update RESULTS.md + RELEASE-BLURB.md, run make gates, and commit."
