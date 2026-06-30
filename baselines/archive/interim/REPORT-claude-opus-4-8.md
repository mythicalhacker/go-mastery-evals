# Go Mastery — Eval Report

## Provenance

- **Model:** claude-opus-4-8
- **Runner:** anthropic
- **Temperature (applied):** not applied — model rejected the parameter
- **Samples / (case,variant):** 5
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:4a0234e6d65e (content)
- **Cases graded:** 17
- **Generated (UTC):** 2026-06-25 14:25:02Z

## Per-case results (passes / samples)

| Case | Category | with | without |
|---|---|---|---|
| concurrency-bounded-parallelism | concurrency | 5/5 | 5/5 |
| concurrency-deadline-propagation | concurrency | 5/5 | 5/5 |
| concurrency-pipeline-cancel | concurrency | 5/5 | 5/5 |
| concurrency-search-leak | concurrency | 5/5 | 5/5 |
| concurrency-select-done | concurrency | 5/5 | 5/5 |
| concurrency-worker-ctx | concurrency | 5/5 | 5/5 |
| correctness-parsesize | correctness | 5/5 | 5/5 |
| errors-wrapping | errors | 5/5 | 5/5 |
| http-timeouts | api-design | 5/5 | 5/5 |
| modern-errors-astype | modernization | 5/5 | 0/5 |
| modern-maps-iter | modernization | 5/5 | 5/5 |
| modern-omitzero | modernization | 5/5 | 5/5 |
| modern-rand-v2 | modernization | 5/5 | 5/5 |
| modern-range-int | modernization | 5/5 | 5/5 |
| modern-slices-contains | modernization | 5/5 | 5/5 |
| modern-waitgroup-go | modernization | 5/5 | 5/5 |
| security-sql-injection | security | 5/5 | 5/5 |

## Summary

- **with**: pass@1 100% (17/17 cases pass)
- **without**: pass@1 94% (16/17 cases pass)

- **Lift (pass@1, with − without): +5.9 pp**

## By category

| Category | with pass@1 | without pass@1 | lift |
|---|---|---|---|
| api-design | 100% | 100% | +0 pp |
| concurrency | 100% | 100% | +0 pp |
| correctness | 100% | 100% | +0 pp |
| errors | 100% | 100% | +0 pp |
| modernization | 100% | 86% | +14 pp |
| security | 100% | 100% | +0 pp |
