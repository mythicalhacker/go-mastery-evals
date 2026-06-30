"""Aggregate graded results into reports (markdown + JSON).

Multi-model & sample-aware. Each result row carries a ``model`` id (one run can
A/B several model tiers in a single invocation) and a ``sample`` index
(``--samples N`` grades each (case, variant) N times).

Outputs:
  * ``results/REPORT.md``        — a cross-model matrix, one row per model:
    with/without pass@1, lift, **corrective rate** (of cases the base model fails
    *without* the skill, the fraction the skill fixes) and **regression count**
    (cases that pass *without* the skill but fail *with* it — should be ~0; a long
    skill prompt can hurt a weak tier, so any regression is flagged prominently).
  * ``results/REPORT-<model>.md`` — per-model detail (per-case table, summary,
    by-category). ``category`` is a DOMAIN label only (no control exclusion).
  * ``results/results.json``     — machine-readable shared provenance + per-model
    metrics + all raw rows.

A case "passes" a variant when a majority of its samples passed; at the CI
default (temperature 0, samples 1) that is exact pass/fail.
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path


def _safe(name: str) -> str:
    """Filesystem-safe slug for a model id (used in REPORT-<model>.md / raw/)."""
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(name))


def _aggregate(results):
    """case_id -> variant -> list[bool] of per-attempt pass/fail."""
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in results:
        by[r["case_id"]][r["variant"]].append(bool(r["passed"]))
    return by


def _rates(by, variant):
    """case_id -> pass rate for `variant` (cases that have at least one attempt)."""
    return {cid: sum(a) / len(a) for cid, cv in by.items() if (a := cv.get(variant))}


def _case_passed(rate):
    """Majority vote; exact pass/fail at the CI default (temp 0, samples 1)."""
    return rate >= 0.5


def _model_metrics(by):
    """with/without pass@1, lift, corrective rate, regression list for one model."""
    w, wo = _rates(by, "with"), _rates(by, "without")
    cmp_ids = sorted(set(w) & set(wo))  # cases comparable on both variants
    with_p1 = sum(w[c] for c in cmp_ids) / len(cmp_ids) if cmp_ids else 0.0
    without_p1 = sum(wo[c] for c in cmp_ids) / len(cmp_ids) if cmp_ids else 0.0
    without_fail = [c for c in cmp_ids if not _case_passed(wo[c])]
    fixed = [c for c in without_fail if _case_passed(w[c])]
    corrective = (len(fixed) / len(without_fail)) if without_fail else None
    regressions = [c for c in cmp_ids if _case_passed(wo[c]) and not _case_passed(w[c])]
    # Head-to-head vs a competitor skill, if that variant was run. Compare our skill
    # and the competitor on the SAME cases (where both have attempts).
    comp = _rates(by, "competitor")
    co_ids = sorted(set(w) & set(comp))
    competitor_p1 = sum(comp[c] for c in co_ids) / len(co_ids) if co_ids else None
    with_over_co = sum(w[c] for c in co_ids) / len(co_ids) if co_ids else None
    ours_only = [c for c in co_ids if _case_passed(w[c]) and not _case_passed(comp[c])]
    theirs_only = [c for c in co_ids if _case_passed(comp[c]) and not _case_passed(w[c])]
    return {
        "n_cases": len(cmp_ids),
        "with_pass_at_1": with_p1,
        "without_pass_at_1": without_p1,
        "lift_pp": 100 * (with_p1 - without_p1),
        "corrective_fixed": len(fixed),
        "corrective_of": len(without_fail),
        "corrective_rate": corrective,
        "regression_count": len(regressions),
        "regression_ids": regressions,
        "competitor_n": len(co_ids),
        "competitor_pass_at_1": competitor_p1,
        "with_over_competitor_p1": with_over_co,
        "vs_competitor_pp": (100 * (with_over_co - competitor_p1)) if competitor_p1 is not None else None,
        "ours_only_ids": ours_only,
        "theirs_only_ids": theirs_only,
    }


def _provenance_block(p, order):
    if not p:
        return []
    lines = ["## Provenance", ""]
    for key, label in order:
        if key in p and p[key] is not None:
            lines.append(f"- **{label}:** {p[key]}")
    lines.append("")
    return lines


# --------------------------------------------------------------------------- #
# Per-model detailed report                                                   #
# --------------------------------------------------------------------------- #

def _model_report_lines(by, cases, variants, provenance, quality=None):
    category = {c["id"]: c.get("category", "") for c in cases}
    lines = ["# Go Mastery — Eval Report", ""]
    lines += _provenance_block(provenance, [
        ("model", "Model"),
        ("runner", "Runner"),
        ("temperature", "Temperature (applied)"),
        ("samples", "Samples / (case,variant)"),
        ("go_version", "Go toolchain"),
        ("skill_fingerprint", "Skill fingerprint"),
        ("n_cases", "Cases graded"),
        ("timestamp_utc", "Generated (UTC)"),
    ])

    # Per-case table (k/N passes per variant).
    lines += [
        "## Per-case results (passes / samples)",
        "",
        "| Case | Category | " + " | ".join(variants) + " |",
        "|---|---|" + "|".join(["---"] * len(variants)) + "|",
    ]
    for cid in sorted(by):
        row = [cid, category.get(cid, "")]
        for v in variants:
            a = by[cid].get(v)
            row.append(f"{sum(a)}/{len(a)}" if a else "-")
        lines.append("| " + " | ".join(row) + " |")

    # Summary — over all cases (category is a domain label, not an exclusion).
    lines += ["", "## Summary", ""]
    rate = {}
    for v in variants:
        rv = _rates(by, v)
        rate[v] = sum(rv.values()) / len(rv) if rv else 0.0
        passed = sum(1 for x in rv.values() if _case_passed(x))
        lines.append(f"- **{v}**: pass@1 {100 * rate[v]:.0f}% "
                     f"({passed}/{len(rv)} cases pass)")
    if "with" in rate and "without" in rate:
        lines.append("")
        lines.append(f"- **Lift (pass@1, with − without): "
                     f"{100 * (rate['with'] - rate['without']):+.1f} pp**")

    # By category (domain breakdown).
    lines += ["", "## By category", ""]
    has_ab = {"with", "without"} <= set(variants)
    lines.append("| Category | " + " | ".join(f"{v} pass@1" for v in variants)
                 + (" | lift |" if has_ab else " |"))
    lines.append("|---|" + "|".join(["---"] * len(variants)) + ("|---|" if has_ab else "|"))
    for cat in sorted({c.get("category", "") for c in cases}):
        ids = {c["id"] for c in cases if c.get("category", "") == cat}
        cat_by = {cid: by[cid] for cid in ids if cid in by}
        cells, per_v = [], {}
        for v in variants:
            rs = [sum(a) / len(a) for cid in cat_by if (a := cat_by[cid].get(v))]
            per_v[v] = sum(rs) / len(rs) if rs else None
            cells.append(f"{100 * per_v[v]:.0f}%" if per_v[v] is not None else "-")
        row = f"| {cat or '(none)'} | " + " | ".join(cells)
        if has_ab:
            if per_v.get("with") is not None and per_v.get("without") is not None:
                row += f" | {100 * (per_v['with'] - per_v['without']):+.0f} pp |"
            else:
                row += " | - |"
        else:
            row += " |"
        lines.append(row)

    # Deterministic quality, per case — shows WHAT improved (idiom hits/misses), so a
    # human can read the with-vs-without delta even where correctness is saturated.
    if quality:
        lines += ["", "## Quality by case (deterministic)", "",
                  "Idiom adoption − anti-patterns on comment-stripped code (per-case rubrics).",
                  "",
                  "| Case | with | without | Δ | with: idioms present | with: idioms missing |",
                  "|---|---|---|---|---|---|"]
        for cid in sorted(quality):
            qd = quality[cid]
            w, wo = qd.get("with"), qd.get("without")
            ws = f"{w['mean']:+.1f}" if w else "-"
            wos = f"{wo['mean']:+.1f}" if wo else "-"
            delta = f"{w['mean'] - wo['mean']:+.1f}" if w and wo else "-"
            hits = ", ".join(w["hits"][:6]) if w else ""
            miss = ", ".join(w["misses"][:6]) if w else ""
            lines.append(f"| {cid} | {ws} | {wos} | {delta} | {hits} | {miss} |")
    return lines


# --------------------------------------------------------------------------- #
# Top-level: cross-model matrix + per-model files                             #
# --------------------------------------------------------------------------- #

def _quality_data(raw_dir, cases):
    """Deterministic quality from results/raw: returns (q, rates) keyed (model,case,variant),
    or (None, None) if raw is unavailable. Imported lazily so the report renders without
    the quality layer (e.g. synthetic test runs with no raw dir)."""
    if not raw_dir or not Path(raw_dir).is_dir():
        return None, None
    from harness import quality  # noqa: PLC0415 — lazy; keeps render() usable sans raw
    cmap = {c["id"]: c for c in cases}
    q = quality.score_raw_dir(raw_dir, cmap)
    return (q, quality) if q else (None, None)


def render(results, cases, out_dir, provenance=None, model_meta=None, raw_dir=None):
    """model_meta: optional {model_id: temperature_value_or_note} overriding the
    per-model 'Temperature (applied)' line — so a model that ran *without*
    temperature (rejected) reports that honestly instead of the requested value.
    raw_dir: results/raw; when present, a deterministic quality section is added."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    provenance = provenance or {}
    model_meta = model_meta or {}

    models = [m for m in dict.fromkeys(r.get("model", "(unknown)") for r in results)]
    variants = sorted({r["variant"] for r in results})

    q, quality = _quality_data(raw_dir, cases)

    per_model = {}      # model -> {"by":..., "metrics":..., "report_file":...}
    for m in models:
        rows = [r for r in results if r.get("model", "(unknown)") == m]
        by = _aggregate(rows)
        metrics = _model_metrics(by)
        mprov = dict(provenance, model=m, n_cases=metrics["n_cases"])
        if m in model_meta and model_meta[m] is not None:
            mprov["temperature"] = model_meta[m]
        # Per-case quality for this model: {case: {variant: {mean, hits, misses}}}.
        mq = None
        if q is not None:
            mq = collections.defaultdict(dict)
            for (mm, cid, v), x in q.items():
                if mm == m:
                    mq[cid][v] = x
        fname = f"REPORT-{_safe(m)}.md"
        (out / fname).write_text(
            "\n".join(_model_report_lines(by, cases, variants, mprov, mq)) + "\n")
        per_model[m] = {"by": by, "metrics": metrics, "report_file": fname}

    # ---- Cross-model matrix (results/REPORT.md) ----------------------------
    has_ab = {"with", "without"} <= set(variants)
    lines = ["# Go Mastery — Eval Report (cross-model)", ""]
    lines += _provenance_block(provenance, [
        ("models", "Models"),
        ("runner", "Runner"),
        ("temperature", "Temperature (requested)"),
        ("samples", "Samples / (case,variant)"),
        ("go_version", "Go toolchain"),
        ("skill_fingerprint", "Skill fingerprint"),
        ("timestamp_utc", "Generated (UTC)"),
    ])

    if has_ab:
        lines += [
            "## Cross-model matrix",
            "",
            "Corrective = of cases the base model fails *without* the skill, the "
            "fraction the skill fixes. Regressions = passed *without* but failed "
            "*with* (want 0).",
            "",
            "| Model | cases | with pass@1 | without pass@1 | lift | corrective | regressions |",
            "|---|---|---|---|---|---|---|",
        ]
        flagged = []
        for m in models:
            mt = per_model[m]["metrics"]
            corr = mt["corrective_rate"]
            corr_s = (f"{mt['corrective_fixed']}/{mt['corrective_of']} "
                      f"({100 * corr:.0f}%)") if corr is not None else "n/a"
            reg = mt["regression_count"]
            reg_s = f"**{reg}** ⚠️" if reg > 0 else "0"
            if reg > 0:
                flagged.append((m, mt["regression_ids"]))
            lines.append(
                f"| {m} | {mt['n_cases']} | {100 * mt['with_pass_at_1']:.0f}% | "
                f"{100 * mt['without_pass_at_1']:.0f}% | {mt['lift_pp']:+.1f} pp | "
                f"{corr_s} | {reg_s} |")
        if flagged:
            lines += ["", "### ⚠️ Regressions detected (skill made the base model worse)"]
            for m, ids in flagged:
                lines.append(f"- **{m}**: {', '.join(ids)}")
        comp_models = [m for m in models
                       if per_model[m]["metrics"].get("competitor_pass_at_1") is not None]
        if comp_models:
            lines += [
                "", "## Head-to-head vs competitor skill", "",
                "Our skill vs the competitor (`competitor` variant) on the same cases. "
                "`only we pass` / `only they pass` count cases one skill gets right and the "
                "other doesn't.",
                "",
                "| Model | cases | our pass@1 | competitor pass@1 | us − competitor | only we pass | only they pass |",
                "|---|---|---|---|---|---|---|",
            ]
            for m in comp_models:
                mt = per_model[m]["metrics"]
                lines.append(
                    f"| {m} | {mt['competitor_n']} | {100 * mt['with_over_competitor_p1']:.0f}% | "
                    f"{100 * mt['competitor_pass_at_1']:.0f}% | {mt['vs_competitor_pp']:+.1f} pp | "
                    f"{len(mt['ours_only_ids'])} | {len(mt['theirs_only_ids'])} |")
    else:
        lines += ["## Results", "",
                  "_Only one variant present; need both `with` and `without` for lift._"]

    # ---- Quality (deterministic) — the strong-tier read where correctness saturates --
    if q is not None:
        rates = {}
        for m in models:
            for v in variants:
                for cid, rate in _rates(per_model[m]["by"], v).items():
                    rates[(m, cid, v)] = rate
        lines += [
            "", "## Quality (deterministic)", "",
            "Idiom adoption − anti-patterns on comment-stripped code (per-case rubrics; no "
            "API, fully reproducible). `both-pass` = each variant's pass-rate ≥ 0.6 — quality "
            "lift on already-correct code, the signal that survives when pass/fail saturates.",
            "",
            "| Model | quality with | quality without | Δquality (all) | Δquality (both-pass) | n both-pass |",
            "|---|---|---|---|---|---|",
        ]
        for m in models:
            wv = [x["mean"] for (mm, _c, v), x in q.items() if mm == m and v == "with"]
            ov = [x["mean"] for (mm, _c, v), x in q.items() if mm == m and v == "without"]
            qw = sum(wv) / len(wv) if wv else 0.0
            qo = sum(ov) / len(ov) if ov else 0.0
            d_all, d_both, n_both = quality.deltas(q, rates, m)
            lines.append(f"| {m} | {qw:+.2f} | {qo:+.2f} | {d_all:+.2f} | {d_both:+.2f} | {n_both} |")

    lines += ["", "## Per-model detail", ""]
    for m in models:
        lines.append(f"- **{m}** → [`{per_model[m]['report_file']}`]({per_model[m]['report_file']})")

    report_md = out / "REPORT.md"
    report_md.write_text("\n".join(lines) + "\n")

    # ---- results.json ------------------------------------------------------
    summary = {
        "provenance": provenance,
        "models": {
            m: {
                "metrics": per_model[m]["metrics"],
                "per_case": {
                    cid: {v: {"pass": sum(a), "n": len(a)} for v, a in cv.items()}
                    for cid, cv in per_model[m]["by"].items()
                },
            }
            for m in models
        },
    }
    (out / "results.json").write_text(
        json.dumps({"summary": summary, "results": results}, indent=2))
    return report_md
