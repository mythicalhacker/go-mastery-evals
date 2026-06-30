# Eval strategy — testing & setting baselines

How to test the skill and lock baselines **efficiently**, and why we restructured
the process after several issues surfaced later than they should have.

## TL;DR

Gates run cheap → expensive, each gating the next:

| Layer | What it checks | Cost | Command |
|---|---|---|---|
| **L0** apparatus | the *grader itself* — package normalization, non-UTF-8 decode, build-vs-test, `files/`, runner temperature | seconds, **no API** | `python3 -m unittest discover -s tests` |
| **L1** cases | every case discriminates (good→PASS, bad→FAIL) | ~2 min, **no API** | `run_evals.py --validate-cases [--cases-dir …]` |
| **L2** smoke + do-no-harm | 1 tier (Haiku), `samples=1`: skill helps in-domain **and** doesn't drag out-of-domain | minutes, small API | `make smoke` ; `make smoke-harm` |
| **L3** baseline | all cases × 3 tiers × `samples=5` | expensive | `make baseline VERSION=…` |

**Rule: never run L3 to find a bug L0–L2 can find.** L0/L1 on every harness or skill
edit; L2 before any baseline; L3 only when L0–L2 are green.

## Why issues surfaced late (honest retrospective)

Everything that cropped up over the multi-day effort falls into three buckets.

**1. Apparatus bugs — surfaceable on day one, zero API.** The package-collision
(`package main` vs `package solution`), the non-UTF-8 decode crash, `build` defaulting
to true (bottle-song), and a broken `competitor_dir` attribute. These hid because:

- The unit tests covered the **pure-Python text layer** (`extract_code`,
  `strip_comments`, regex matching) thoroughly, but **never the toolchain-integration
  layer** (normalize → build → test → decode) where all of these lived. The tests were
  deliberately "stdlib-only, run anywhere" — which meant the layer that actually breaks
  on real model output was never executed by a test.
- Fixtures were **pristine**: our hand-authored `good`/`bad` solutions always used
  `package solution` and ASCII output, so `--validate-cases` passed with false
  confidence — it never reproduced what a real model emits (alt package names, missing
  symbols, raw bytes).
- `make gates` did run `unittest discover`, but the runner tests had silently broken
  and weren't being watched, so even an existing test wasn't protecting us.

**2. Case-quality issues — caught correctly, on time.** The refactoring / pre-implemented
Aider stubs (`counter`, `ledger`, `markdown`) were flagged by `--validate-cases` the
moment we staged them. The process worked here; no change needed.

**3. Behavioral / out-of-domain effects — genuinely need generations.** Attention
dilution on Haiku and the exact-API artifact (protein-translation) cannot be caught
offline. But we discovered them via the **most expensive run** (full suite × 3 tiers),
because there was no cheap smoke gate and no out-of-domain track until the very end.

**Root causes:** (a) we tested the *skill* but under-tested the *measuring instrument*;
(b) clean fixtures ≠ real output; (c) no cheap early gate, so the first signal for any
behavioral issue was a multi-hundred-call run; (d) bottom-up growth — each new case
*type* (niche/ext template, cross-build, external/Aider) exercised a grader path that
had never run, surfacing one latent bug per expansion.

**What was genuinely unavoidable:** the out-of-domain behavioral findings needed real
generations. But a do-no-harm canary on Haiku would have shown the *direction* in
minutes instead of a full 3-tier run — so even these were surfaceable far sooner.

## Baselines

- **Set:** `make baseline VERSION=<name>` runs L3 and snapshots `REPORT*.md` +
  `results.json` + a `MANIFEST.txt` (version, date, models, samples, **skill
  fingerprint**, git SHA, go version) into `baselines/<name>/`.
- **Guard:** `make compare BASE=<name>` diffs the latest run against the locked baseline,
  prints per-model with-skill pass deltas, and **exits non-zero if any case that passed
  with the skill in the baseline fails now.** This is what prevents silent regressions
  across iteration.
- Every baseline is tied to a skill fingerprint; **editing `SKILL.md` ⇒ new baseline.**

## Do-no-harm canary

A small permanent slice run in L2 on **Haiku** (weakest tier = dilution shows first):

- **In-domain** (must help or hold): `concurrency-detach-context`, `errors-join-aggregate`,
  `security-sql-injection`, `modern-errors-astype`, `mcp-current-sdk`, `correctness-slice-aliasing`.
- **Out-of-domain** (must not drag): `aider-variable-length-quantity` (the one case that
  genuinely regressed), `aider-protein-translation`, `aider-matrix`, `aider-hexadecimal`,
  `aider-crypto-square`, `aider-two-bucket`.

Seeding the canary with the cases that actually regressed makes the gate specifically
guard the failure modes we found.

## Measuring quality, not just correctness (the strong-tier problem)

Binary pass/fail is the wrong instrument on a strong model. Opus passes most cases
**with and without** the skill, so correctness lift reads ~0 — but the skill still
changes the *code*. We measure that directly with a **deterministic quality score**
(`harness/quality.py`, `make quality`): idiom adoption minus anti-patterns, scored
on comment-stripped source. No model, no sampling, no API — so it's reproducible and
**free to recompute** (generate once, score forever; iterate the rubric offline).

Evidence on data already generated — six Opus cases that pass **5/5 both ways**
(zero behavioral lift) yet differ in quality:

| case | pass with | pass w/o | qual with | qual w/o |
|---|---|---|---|---|
| security-sql-injection | 5/5 | 5/5 | 3.0 | 1.0 |
| performance-pool-reset | 5/5 | 5/5 | 0.0 | −1.0 |
| modern-maps-clone | 5/5 | 5/5 | 1.0 | 0.0 |

**Per tier, one framework, tier-appropriate axis:**

- **Haiku** — correctness lift is the headline (it has headroom: +21pp). *Also* watch
  context dilution: the always-on core can drag a weak model (references are
  lazy-loaded; the always-on `SKILL.md` is what dilutes — keep it lean). Quality is
  the secondary read.
- **Sonnet** — both correctness lift and quality delta.
- **Opus** — quality delta is the headline; correctness is saturated.

**Determinism.** The quality layer is fully deterministic. For the behavioral layer
(temp-0 is *not* deterministic on the API), the fixes are: report **pass-rate (k/n)**,
not binary majority; set **tolerances** in `make compare` so a 4/5↔5/5 flip is not a
"regression"; and **generate-once/score-many** so analysis is reproducible. A baseline
is a vector of `(pass-rate, quality-score)` with tolerances — it stops wobbling on a
single-sample flip.

**Shipped (production-grade).** All of the above is implemented and tested
(`tests/test_quality.py`, `tests/test_compare.py`):

- **Per-case rubrics** — `case.yaml: quality_signals` with `positive`/`negative` patterns
  that ADD to the global rubric and a `disable` list that trims it. Relevant idioms differ
  by case (http→timeouts, db→parameterized, concurrency→ctx); a case without the block uses
  the global rubric unchanged (backward compatible). `quality.score_detail(code, case)`
  returns `{score, hits, misses}` so the report shows *what* improved, not just a number.
- **Deterministic non-regex dimensions** — `golangci-lint` issue count (int, not pass/fail)
  and gofmt-clean fold into a composite `quality = idiom − LINT_WEIGHT*issues + GOFMT_BONUS`
  (named constants). The Go-dependent dimensions **skip gracefully** when Go / golangci-lint
  are absent (the term drops; the value falls back to the idiom score), so the whole layer is
  pure-Python deterministic and runs offline with no API.
- **Report** — `REPORT.md` has a `## Quality (deterministic)` cross-model table (quality
  with/without, Δ all, Δ both-pass, n both-pass); each `REPORT-<model>.md` has a per-case
  quality table with idiom hit/miss labels. Pass-*rate* (not binary majority) is the machine
  metric.
- **Noise-tolerant `compare`** — a baseline is a `(pass_rate, quality)` vector
  (`baseline-metrics.json`, written by `make baseline` so old baselines need no kept raw).
  `make compare` flags a **correctness** regression only when with-skill pass-rate drops
  `> --pass-tol` (default 0.2 — a 4/5↔5/5 flip is 0.2, NOT greater, so it's ignored) and a
  **quality** regression when quality drops `> --quality-tol` (default 0.5) on a case that
  *still passes*. Exit non-zero only on an out-of-tolerance regression.
- **`make quality` / `make quality-panel`** — score the corpus from `results/raw` (no API);
  the panel lists cases with a non-zero Δquality — the small set worth regenerating on Opus
  via `--only`.

## Efficiency notes

- `samples=1` for smoke (direction); `samples=5` only for the baseline (noise control
  where it's reported). At `samples=3` on ~36 hard cases, ±2 cases is within sampling
  noise — don't over-read small lifts.
- Grading is offline (`-mod=vendor`, `GOPROXY=off`) on a warm `GOCACHE`; the slow part is
  the per-grade vendored-template copy. A future `--jobs N` to parallelize
  generation+grading (currently serial) would cut wall-clock the most.
- Keep `_aider-src` / `cases-aider` regenerable and git-ignored; `stage_aider.py` rebuilds them.

## Map: each past bug → the layer that now catches it

| Bug | Now caught by |
|---|---|
| package collision (alt package name) | L0 `test_alt_package_name_is_normalized` |
| non-UTF-8 decode crash | L0 `test_non_utf8_test_output_does_not_crash` |
| `build` vs `test` (test-defined helper) | L0 `test_build_excludes_test_helpers_but_test_includes_them` |
| multi-test-file (`cases_test.go`) | L0 `test_extra_test_file_in_files_dir_is_compiled` |
| broken `competitor_dir` attribute | L0 `tests/test_runners.py` (now green under `discover`) |
| refactoring/pre-implemented stubs | L1 `--validate-cases` (+ `stage_aider.py` SKIP list) |
| out-of-domain dilution / API artifacts | L2 `make smoke-harm` (Haiku canary) before L3 |
