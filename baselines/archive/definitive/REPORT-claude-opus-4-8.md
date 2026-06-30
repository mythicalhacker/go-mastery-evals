# Go Mastery — Eval Report

## Provenance

- **Model:** claude-opus-4-8
- **Runner:** anthropic
- **Temperature (applied):** not applied — model rejected the parameter
- **Samples / (case,variant):** 5
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:4a0234e6d65e (content)
- **Cases graded:** 24
- **Generated (UTC):** 2026-06-26 14:32:31Z

## Per-case results (passes / samples)

| Case | Category | with | without |
|---|---|---|---|
| concurrency-bounded-parallelism | concurrency | 5/5 | 5/5 |
| concurrency-deadline-propagation | concurrency | 5/5 | 5/5 |
| concurrency-pipeline-cancel | concurrency | 5/5 | 5/5 |
| concurrency-search-leak | concurrency | 5/5 | 5/5 |
| concurrency-select-done | concurrency | 5/5 | 4/5 |
| concurrency-worker-ctx | concurrency | 5/5 | 5/5 |
| correctness-concurrent-map | correctness | 5/5 | 5/5 |
| correctness-lost-update | correctness | 5/5 | 5/5 |
| correctness-parsesize | correctness | 5/5 | 5/5 |
| correctness-slice-aliasing | correctness | 5/5 | 5/5 |
| correctness-time-equal | correctness | 5/5 | 5/5 |
| errors-wrapping | errors | 5/5 | 5/5 |
| frontier-errors-astype-2 | modernization | 5/5 | 0/5 |
| http-timeouts | api-design | 5/5 | 5/5 |
| modern-errors-astype | modernization | 5/5 | 0/5 |
| modern-maps-iter | modernization | 5/5 | 5/5 |
| modern-new-expr | modernization | 5/5 | 0/5 |
| modern-omitzero | modernization | 5/5 | 5/5 |
| modern-rand-v2 | modernization | 5/5 | 5/5 |
| modern-range-int | modernization | 4/5 | 5/5 |
| modern-slices-contains | modernization | 5/5 | 5/5 |
| modern-waitgroup-go | modernization | 5/5 | 5/5 |
| niche-singleflight | concurrency | 5/5 | 5/5 |
| security-sql-injection | security | 5/5 | 5/5 |

## Summary

- **with**: pass@1 99% (24/24 cases pass)
- **without**: pass@1 87% (21/24 cases pass)

- **Lift (pass@1, with − without): +12.5 pp**

## By category

| Category | with pass@1 | without pass@1 | lift |
|---|---|---|---|
| api-design | 100% | 100% | +0 pp |
| concurrency | 100% | 97% | +3 pp |
| correctness | 100% | 100% | +0 pp |
| errors | 100% | 100% | +0 pp |
| modernization | 98% | 67% | +31 pp |
| security | 100% | 100% | +0 pp |
