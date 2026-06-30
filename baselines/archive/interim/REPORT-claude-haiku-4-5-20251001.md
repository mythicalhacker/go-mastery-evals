# Go Mastery — Eval Report

## Provenance

- **Model:** claude-haiku-4-5-20251001
- **Runner:** anthropic
- **Temperature (applied):** 0.0
- **Samples / (case,variant):** 5
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:4a0234e6d65e (content)
- **Cases graded:** 17
- **Generated (UTC):** 2026-06-25 14:25:02Z

## Per-case results (passes / samples)

| Case | Category | with | without |
|---|---|---|---|
| concurrency-bounded-parallelism | concurrency | 0/5 | 5/5 |
| concurrency-deadline-propagation | concurrency | 5/5 | 5/5 |
| concurrency-pipeline-cancel | concurrency | 5/5 | 5/5 |
| concurrency-search-leak | concurrency | 5/5 | 5/5 |
| concurrency-select-done | concurrency | 5/5 | 5/5 |
| concurrency-worker-ctx | concurrency | 5/5 | 5/5 |
| correctness-parsesize | correctness | 1/5 | 0/5 |
| errors-wrapping | errors | 5/5 | 5/5 |
| http-timeouts | api-design | 5/5 | 5/5 |
| modern-errors-astype | modernization | 5/5 | 0/5 |
| modern-maps-iter | modernization | 5/5 | 5/5 |
| modern-omitzero | modernization | 5/5 | 0/5 |
| modern-rand-v2 | modernization | 5/5 | 5/5 |
| modern-range-int | modernization | 5/5 | 0/5 |
| modern-slices-contains | modernization | 5/5 | 5/5 |
| modern-waitgroup-go | modernization | 5/5 | 0/5 |
| security-sql-injection | security | 5/5 | 5/5 |

## Summary

- **with**: pass@1 89% (15/17 cases pass)
- **without**: pass@1 71% (12/17 cases pass)

- **Lift (pass@1, with − without): +18.8 pp**

## By category

| Category | with pass@1 | without pass@1 | lift |
|---|---|---|---|
| api-design | 100% | 100% | +0 pp |
| concurrency | 83% | 100% | -17 pp |
| correctness | 20% | 0% | +20 pp |
| errors | 100% | 100% | +0 pp |
| modernization | 100% | 43% | +57 pp |
| security | 100% | 100% | +0 pp |
