#!/usr/bin/env python3
"""Compare a new eval run against a locked baseline — NOISE-TOLERANT.

temp-0 is not deterministic on the API, so a binary majority verdict wobbles: a
4/5↔5/5 flip looks like a regression when it's sampling noise. So a baseline here is
a vector of ``(pass_rate, quality_score)`` per (model, case), and a regression must
clear a TOLERANCE:

  * correctness regression — with-skill ``pass_rate`` dropped by MORE THAN ``--pass-tol``
    (default 0.2: at n=5 a single-sample flip = 0.2, which is NOT > 0.2, so it's ignored).
  * quality regression — with-skill ``quality`` dropped by MORE THAN ``--quality-tol``
    (default 0.5) on a case that STILL passes (so we flag "passes but got worse", the
    thing that hides from binary pass/fail).

Exit code 0 if clean, 1 only on an out-of-tolerance regression — so a single-sample
flip never trips `make compare`.

Usage:
    python3 harness/compare_baseline.py <baseline_dir_or_results.json> <new_results.json>
"""
from __future__ import annotations
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from harness import quality as Q  # noqa: E402

PASS_TOL = 0.2      # at n=5, one-sample flip = 0.2; regression needs a drop strictly greater
QUALITY_TOL = 0.5
STILL_PASSES = Q.BOTH_PASS_RATE  # quality regressions only count where the new run still passes


def _with(d, model, case, key):
    """base/new[model][case]['with'][key] or None, tolerating missing levels."""
    return ((d.get(model) or {}).get(case) or {}).get("with", {}).get(key)


def compare(base, new, pass_tol=PASS_TOL, quality_tol=QUALITY_TOL):
    """Diff two metric vectors {model:{case:{variant:{pass_rate,quality}}}}.

    Returns (corr_regs, qual_regs, rows): the two regression lists (each
    ``(model, case, before, after)``) and a per-model summary table
    ``(model, corr_delta, qual_delta, n)``. Pure function — no files, no Go."""
    corr_regs, qual_regs, rows = [], [], []
    for m in sorted(set(base) | set(new)):
        cases = sorted(set((base.get(m) or {})) | set((new.get(m) or {})))
        corr_deltas, qual_deltas = [], []
        for c in cases:
            bpr, npr = _with(base, m, c, "pass_rate"), _with(new, m, c, "pass_rate")
            if bpr is not None and npr is not None:
                corr_deltas.append(npr - bpr)
                if (npr - bpr) < -pass_tol:
                    corr_regs.append((m, c, bpr, npr))
            bq, nq = _with(base, m, c, "quality"), _with(new, m, c, "quality")
            if bq is not None and nq is not None:
                qual_deltas.append(nq - bq)
                # only a regression if the case still passes (else correctness already flags it)
                if npr is not None and npr >= STILL_PASSES and (nq - bq) < -quality_tol:
                    qual_regs.append((m, c, bq, nq))
        cd = sum(corr_deltas) / len(corr_deltas) if corr_deltas else 0.0
        qd = sum(qual_deltas) / len(qual_deltas) if qual_deltas else 0.0
        rows.append((m, cd, qd, len(cases)))
    return corr_regs, qual_regs, rows


def _load_metrics(path, cmap):
    """Metrics for one side. A baselines/<ver>/ dir prefers its computed
    ``baseline-metrics.json`` (so old baselines need no raw kept); otherwise compute
    from results.json + a sibling raw/ dir (quality is None when raw is absent)."""
    import json
    p = pathlib.Path(path)
    if p.is_dir():
        bm = p / "baseline-metrics.json"
        if bm.exists():
            return json.loads(bm.read_text())
        return Q.metrics(str(p / "results.json"), str(p / "raw"), cmap)
    return Q.metrics(str(p), str(p.parent / "raw"), cmap)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base", help="baselines/<ver> dir, or a results.json")
    ap.add_argument("new", help="new results.json (or its dir)")
    ap.add_argument("--pass-tol", type=float, default=PASS_TOL)
    ap.add_argument("--quality-tol", type=float, default=QUALITY_TOL)
    ap.add_argument("--cases-dir", default="cases")
    ap.add_argument("--aider-dir", default="cases-aider")
    a = ap.parse_args(argv[1:])

    cmap = Q.load_case_map(a.cases_dir, a.aider_dir)
    base, new = _load_metrics(a.base, cmap), _load_metrics(a.new, cmap)
    corr_regs, qual_regs, rows = compare(base, new, a.pass_tol, a.quality_tol)

    print(f"Comparing  base={a.base}  vs  new={a.new}"
          f"   (pass-tol={a.pass_tol}, quality-tol={a.quality_tol})\n")
    print(f"{'model':<32}{'Δ pass-rate':>13}{'Δ quality':>11}{'cases':>8}")
    for m, cd, qd, n in rows:
        print(f"{m:<32}{cd:>+13.2f}{qd:>+11.2f}{n:>8}")

    if corr_regs:
        print(f"\nCORRECTNESS regressions ({len(corr_regs)}) — with-skill pass-rate dropped > {a.pass_tol}:")
        for m, c, b, n in corr_regs:
            print(f"  - {m} · {c}: {b:.2f} -> {n:.2f}")
    if qual_regs:
        print(f"\nQUALITY regressions ({len(qual_regs)}) — still passing but quality dropped > {a.quality_tol}:")
        for m, c, b, n in qual_regs:
            print(f"  - {m} · {c}: {b:+.2f} -> {n:+.2f}")
    if corr_regs or qual_regs:
        print("\nFAIL: new run regresses against the baseline (beyond tolerance).")
        return 1
    print("\nOK: no out-of-tolerance regression vs the baseline "
          "(single-sample flips are within tolerance).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
