#!/usr/bin/env python3
"""Deterministic code-quality scoring — the metric for strong models.

Behavioral pass/fail SATURATES on a strong model: Opus passes with *and* without
the skill, so correctness shows ~0 lift even when the skill clearly improves the
code. Quality answers "is the code better?" when both pass.

Design choices that address the three things wrong with binary pass/fail:
  * GRADED, not binary — a score with resolution, so strong tiers aren't flat.
  * DETERMINISTIC — scored from the emitted code alone (idiom adoption minus
    anti-patterns, on comment-stripped source). No model, no sampling, no API.
  * FREE to recompute — generate once, score forever; iterate the rubric offline.

The idiom score is the always-available, pure-Python core. A richer COMPOSITE folds
in deterministic toolchain dimensions (golangci-lint issue count, gofmt-clean) when
Go is present; absent Go, those dimensions skip gracefully and the composite equals
the idiom score — so this module never needs the API and never hard-fails offline.

Per-case rubrics: a case.yaml may carry a ``quality_signals`` block whose
``positive``/``negative`` patterns ADD to the global rubric and whose ``disable``
list removes named global signals — because the relevant idioms differ by case
(http→timeouts, db→parameterized, concurrency→ctx). Cases without it use the global
rubric unchanged (backward compatible).

Usage:
    python3 harness/quality.py [results/raw] [results/results.json]   # Δquality sweep
    python3 harness/quality.py --panel                                # cases with |Δ|>0
    python3 harness/quality.py --dump-metrics results/raw results/results.json  # baseline metrics
"""
from __future__ import annotations
import argparse
import collections
import json
import pathlib
import re
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from harness.cases import load_cases  # noqa: E402
from harness.grader import extract_code, strip_comments, gofmt_clean, lint_issues  # noqa: E402

# Composite weights (named so the formula is auditable): quality = idiom_score
# − LINT_WEIGHT*lint_issues + (GOFMT_BONUS if gofmt-clean). The Go-dependent terms
# vanish gracefully when the toolchain is absent.
LINT_WEIGHT = 0.5
GOFMT_BONUS = 0.5
BOTH_PASS_RATE = 0.6  # a variant "passes" a case (for both-pass conditioning) at ≥ this rate

# Global rubric. Per-case rubrics (case.yaml `quality_signals`) extend/trim this.
IDIOMS = [
    ("err %w", r"fmt\.Errorf\([^)]*%w"), ("errors.Join", r"errors\.Join\("),
    ("errors.Is/As", r"errors\.(Is|As|AsType)[\(\[]"), ("slog", r"\bslog\."),
    ("slices/maps", r"\b(slices|maps)\."), ("cmp.Or", r"\bcmp\.(Or|Compare)\("),
    ("ctx param", r"ctx\s+context\.Context"), ("defer Close", r"defer\s+[\w.]+\.Close\(\)"),
    ("once/wg.Go", r"sync\.Once(Value|Values)|\.Go\(func"),
]
ANTI = [
    ("interface{}", r"interface\{\}"), ("panic", r"\bpanic\("), ("time.Sleep", r"time\.Sleep\("),
    ("log.Fatal", r"\blog\.Fatal"), ("getter Get", r"func\s+\([^)]*\)\s+Get[A-Z]"),
    ("time.After", r"time\.After\("),
]


def _global_signals():
    pos = [{"label": l, "pattern": r, "weight": 1} for l, r in IDIOMS]
    neg = [{"label": l, "pattern": r, "weight": 1} for l, r in ANTI]
    return pos, neg


def _coerce(sig):
    """A case.yaml signal entry -> normalized {label, pattern, weight}."""
    return {"label": sig.get("label") or sig["pattern"],
            "pattern": sig["pattern"], "weight": sig.get("weight", 1)}


def _merge_signals(case):
    """(positives, negatives) for a case = global, minus its ``disable`` labels, plus
    its per-case ``positive``/``negative``. ``case`` None or rubric-less -> global only."""
    pos, neg = _global_signals()
    qs = (case or {}).get("quality_signals") or {}
    disabled = set(qs.get("disable") or [])
    pos = [s for s in pos if s["label"] not in disabled]
    neg = [s for s in neg if s["label"] not in disabled]
    pos += [_coerce(s) for s in (qs.get("positive") or [])]
    neg += [_coerce(s) for s in (qs.get("negative") or [])]
    return pos, neg


def score_detail(code, case=None):
    """Presence-based idiom score on comment-stripped source. Each signal contributes
    its weight AT MOST ONCE (presence, not frequency). Returns {score, hits, misses}:
    hits = positive labels present (+ ``anti:<label>`` for anti-patterns present),
    misses = positive labels absent. Pure-Python, deterministic, no Go required."""
    c = strip_comments(code or "")
    pos, neg = _merge_signals(case)
    hits, misses, score = [], [], 0
    for s in pos:
        if re.search(s["pattern"], c):
            score += s["weight"]
            hits.append(s["label"])
        else:
            misses.append(s["label"])
    for s in neg:
        if re.search(s["pattern"], c):
            score -= s["weight"]
            hits.append("anti:" + s["label"])
    return {"score": score, "hits": hits, "misses": misses}


def score(code, case=None):
    """Back-compat scalar idiom score (the global rubric by default)."""
    return score_detail(code, case)["score"]


def go_dimensions(code, case, env=None, workroot="/tmp"):
    """Deterministic non-regex dimensions via the Go toolchain. Returns
    {lint_issues:int|None, gofmt_clean:bool|None, skipped:[...]}. Each dimension is
    ``None`` (and named in ``skipped``) when its tool is absent — graceful degradation."""
    lint = lint_issues(case, code, env, workroot)
    fmt = gofmt_clean(case, code, env, workroot)
    skipped = ([] if lint is not None else ["golangci-lint"]) + ([] if fmt is not None else ["gofmt"])
    return {"lint_issues": lint, "gofmt_clean": fmt, "skipped": skipped}


def composite(code, case=None, env=None, workroot="/tmp"):
    """Full composite score: idiom − LINT_WEIGHT*lint_issues + GOFMT_BONUS. Go-dependent
    terms are dropped when their dimension is unavailable, so offline ``quality`` equals
    the deterministic idiom score. Returns the breakdown for transparency."""
    det = score_detail(code, case)
    dims = go_dimensions(code, case, env, workroot)
    q = float(det["score"])
    if dims["lint_issues"] is not None:
        q -= LINT_WEIGHT * dims["lint_issues"]
    if dims["gofmt_clean"]:
        q += GOFMT_BONUS
    return {"quality": q, "idiom": det["score"], "hits": det["hits"], "misses": det["misses"],
            **{k: dims[k] for k in ("lint_issues", "gofmt_clean", "skipped")}}


# --------------------------------------------------------------------------- #
# Corpus scoring (from results/raw — generate once, score forever, no API)     #
# --------------------------------------------------------------------------- #

_RAW_RE = re.compile(r"(.+?)__(.+?)__(with|without|competitor)__s(\d+)\.txt")


def _rows_of(results_json):
    p = pathlib.Path(results_json)
    if not p.exists():
        return []
    d = json.loads(p.read_text())
    return next((v for v in d.values() if isinstance(v, list)), []) if isinstance(d, dict) else d


def _pass_rates(rows):
    """(model, case, variant) -> fraction of samples that passed."""
    g = collections.defaultdict(list)
    for r in rows:
        g[(r["model"], r["case_id"], r["variant"])].append(bool(r["passed"]))
    return {k: sum(v) / len(v) for k, v in g.items()}


def load_case_map(*dirs):
    """{case_id: case} merged across the given case dirs (missing dirs skipped)."""
    out = {}
    for d in dirs:
        if pathlib.Path(d).is_dir():
            for c in load_cases(d):
                out.setdefault(c["id"], c)
    return out


def score_raw_dir(raw_dir, cases_by_id=None):
    """(model, case, variant) -> {mean, n, hits, misses} from raw/*.txt. ``mean`` is the
    mean idiom score across samples; hits/misses are from sample 0 (deterministic)."""
    groups = collections.defaultdict(list)
    for f in pathlib.Path(raw_dir).glob("*.txt"):
        m = _RAW_RE.match(f.name)
        if not m:
            continue
        model, cid, variant, s = m.group(1), m.group(2), m.group(3), int(m.group(4))
        case = (cases_by_id or {}).get(cid)
        groups[(model, cid, variant)].append((s, score_detail(extract_code(f.read_text()), case)))
    out = {}
    for k, lst in groups.items():
        lst.sort(key=lambda x: x[0])
        out[k] = {"mean": statistics.mean(d["score"] for _, d in lst), "n": len(lst),
                  "hits": lst[0][1]["hits"], "misses": lst[0][1]["misses"]}
    return out


def metrics(results_json, raw_dir, cases_by_id=None):
    """Noise-tolerant baseline vector: {model: {case: {variant: {pass_rate, quality}}}}.
    pass_rate from results.json (fraction, not binary); quality = mean idiom score from
    raw (None when raw is unavailable). This is what ``compare`` diffs with tolerances."""
    rates = _pass_rates(_rows_of(results_json))
    q = score_raw_dir(raw_dir, cases_by_id) if raw_dir and pathlib.Path(raw_dir).is_dir() else {}
    out = collections.defaultdict(lambda: collections.defaultdict(dict))
    for (model, cid, variant) in set(rates) | set(q):
        out[model][cid][variant] = {
            "pass_rate": rates.get((model, cid, variant)),
            "quality": q[(model, cid, variant)]["mean"] if (model, cid, variant) in q else None,
        }
    return {m: dict(cv) for m, cv in out.items()}


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #

def deltas(q, rates, model):
    """(Δqual_all, Δqual_both_pass, n_both_pass) for ``model`` from score_raw_dir + pass
    rates. both-pass = each variant's pass_rate ≥ BOTH_PASS_RATE — isolating "quality lift
    on already-correct code", the true Opus signal. Shared by the sweep and the report."""
    alld, bothd = [], []
    for c in sorted({c for (m, c, _) in q if m == model}):
        w, wo = q.get((model, c, "with")), q.get((model, c, "without"))
        if w is None or wo is None:
            continue
        d = w["mean"] - wo["mean"]
        alld.append(d)
        pw, pwo = rates.get((model, c, "with")), rates.get((model, c, "without"))
        if pw is not None and pwo is not None and pw >= BOTH_PASS_RATE and pwo >= BOTH_PASS_RATE:
            bothd.append(d)
    return (statistics.mean(alld) if alld else 0.0,
            statistics.mean(bothd) if bothd else 0.0, len(bothd))


def _sweep(raw_dir, results_json, cmap):
    """Print per-model Δquality (all cases, and both-pass cases) — the strong-tier read."""
    q = score_raw_dir(raw_dir, cmap)
    rates = _pass_rates(_rows_of(results_json))
    print("Quality = idioms adopted − anti-patterns (deterministic, code-only; per-case rubrics applied).")
    print(f"{'model':<30}{'Δqual (all)':>13}{'Δqual (both-pass)':>19}{'n both-pass':>13}")
    for m in sorted({k[0] for k in q}):
        ad, bd, nboth = deltas(q, rates, m)
        print(f"{m:<30}{ad:>+13.2f}{bd:>+19.2f}{nboth:>13}")


def _panel(raw_dir, cmap):
    """Print the case ids with |Δquality| > 0 (union across models) — the small set worth
    regenerating on a strong tier. Re-run them with: run_evals.py ... --only <ids>."""
    q = score_raw_dir(raw_dir, cmap)
    panel = set()
    for (m, c, _) in q:
        w, wo = q.get((m, c, "with")), q.get((m, c, "without"))
        if w and wo and abs(w["mean"] - wo["mean"]) > 0:
            panel.add(c)
    ids = sorted(panel)
    print(f"# quality panel: {len(ids)} case(s) with |Δquality| > 0 (regenerate these on a strong tier)")
    print(",".join(ids) if ids else "(none)")
    if ids:
        print("\nRe-run e.g.:  python3 run_evals.py --runner anthropic --model <opus> "
              "--samples 5 --only " + ",".join(ids))


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("raw", nargs="?", default="results/raw")
    ap.add_argument("results", nargs="?", default="results/results.json")
    ap.add_argument("--panel", action="store_true", help="print case ids with |Δquality|>0")
    ap.add_argument("--dump-metrics", action="store_true",
                    help="write the (pass_rate, quality) metrics vector as JSON to stdout")
    ap.add_argument("--cases-dir", default="cases")
    ap.add_argument("--aider-dir", default="cases-aider")
    a = ap.parse_args(argv[1:])
    # Order-insensitive: the raw arg is a dir, the results arg is a .json file — if the
    # caller swapped them, swap back rather than crashing.
    if pathlib.Path(a.raw).is_file() and pathlib.Path(a.results).is_dir():
        a.raw, a.results = a.results, a.raw
    cmap = load_case_map(a.cases_dir, a.aider_dir)
    if a.dump_metrics:
        json.dump(metrics(a.results, a.raw, cmap), sys.stdout, indent=2, sort_keys=True)
        print()
        return 0
    if a.panel:
        _panel(a.raw, cmap)
        return 0
    _sweep(a.raw, a.results, cmap)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
