# Go Mastery — Eval Report

## Provenance

- **Model:** gpt-5.4-mini
- **Runner:** openai
- **Temperature (applied):** 0.0
- **Samples / (case,variant):** 5
- **Skill fingerprint:** sha256:c3f30e363f88 (content)
- **Cases graded:** 54

## Per-case results (passes / samples)

| Case | Category | with | without |
|---|---|---|---|
| ai-ml-gonum-stat | ai-ml-beyond-llm | 5/5 | 5/5 |
| api-iter-ordered | api-design | 5/5 | 5/5 |
| cgo-c-interop | cgo-and-interop | 5/5 | 5/5 |
| cli-flagset-subcommand | cli | 5/5 | 5/5 |
| cloudnative-reconcile-configmap | cloud-native | 5/5 | 5/5 |
| concurrency-bounded-parallelism | concurrency | 5/5 | 5/5 |
| concurrency-deadline-propagation | concurrency | 5/5 | 5/5 |
| concurrency-detach-context | concurrency | 5/5 | 0/5 |
| concurrency-oncevalues | concurrency | 5/5 | 5/5 |
| concurrency-pipeline-cancel | concurrency | 5/5 | 5/5 |
| concurrency-search-leak | concurrency | 4/5 | 0/5 |
| concurrency-select-done | concurrency | 5/5 | 5/5 |
| concurrency-worker-ctx | concurrency | 5/5 | 5/5 |
| correctness-concurrent-map | correctness | 5/5 | 5/5 |
| correctness-lost-update | correctness | 5/5 | 5/5 |
| correctness-parsesize | correctness | 4/5 | 5/5 |
| correctness-slice-aliasing | correctness | 5/5 | 5/5 |
| correctness-time-equal | correctness | 5/5 | 5/5 |
| database-valuer-scanner | database | 5/5 | 5/5 |
| datastructures-heap | data-structures | 5/5 | 1/5 |
| debugging-all-goroutine-stacks | debugging | 5/5 | 5/5 |
| design-iter-seq | design | 5/5 | 5/5 |
| distributed-consistent-hash | distributed-systems | 5/5 | 5/5 |
| ebpf-current-api | ebpf | 5/5 | 5/5 |
| encoding-json-number | encoding | 5/5 | 5/5 |
| encoding-varint | encoding | 5/5 | 5/5 |
| errors-join-aggregate | errors | 5/5 | 5/5 |
| errors-wrapping | errors | 5/5 | 5/5 |
| event-driven-bus | event-driven | 5/5 | 1/5 |
| file-io-os-root | file-io | 5/5 | 5/5 |
| frontier-errors-astype-2 | modernization | 5/5 | 0/5 |
| generics-filter | generics | 5/5 | 5/5 |
| grpc-interceptor-codes | distributed-systems | 4/5 | 4/5 |
| http-timeouts | api-design | 5/5 | 5/5 |
| internals-runtime-metrics | internals | 5/5 | 5/5 |
| mcp-current-sdk | mcp-and-agents | 5/5 | 0/5 |
| modern-clear-builtin | modern | 5/5 | 0/5 |
| modern-errors-astype | modernization | 4/5 | 0/5 |
| modern-maps-clone | data-structures | 5/5 | 5/5 |
| modern-maps-iter | modernization | 5/5 | 5/5 |
| modern-new-expr | modernization | 5/5 | 0/5 |
| modern-omitzero | modernization | 5/5 | 0/5 |
| modern-rand-v2 | modernization | 5/5 | 5/5 |
| modern-range-int | modernization | 5/5 | 5/5 |
| modern-slices-contains | modernization | 5/5 | 5/5 |
| modern-waitgroup-go | modernization | 5/5 | 0/5 |
| networking-netip | networking | 5/5 | 0/5 |
| niche-singleflight | concurrency | 5/5 | 5/5 |
| observability-otel-span | observability | 5/5 | 5/5 |
| observability-slog-redaction | observability | 5/5 | 5/5 |
| performance-pool-reset | performance | 5/5 | 5/5 |
| security-html-escaping | security | 5/5 | 4/5 |
| security-sql-injection | security | 5/5 | 5/5 |
| wasm-wasip1-build | wasm-and-embedded | 5/5 | 5/5 |

## Summary

- **with**: pass@1 99% (54/54 cases pass)
- **without**: pass@1 78% (42/54 cases pass)

- **Lift (pass@1, with − without): +20.7 pp**

## By category

| Category | with pass@1 | without pass@1 | lift |
|---|---|---|---|
| ai-ml-beyond-llm | 100% | 100% | +0 pp |
| api-design | 100% | 100% | +0 pp |
| cgo-and-interop | 100% | 100% | +0 pp |
| cli | 100% | 100% | +0 pp |
| cloud-native | 100% | 100% | +0 pp |
| concurrency | 98% | 78% | +20 pp |
| correctness | 96% | 100% | -4 pp |
| data-structures | 100% | 60% | +40 pp |
| database | 100% | 100% | +0 pp |
| debugging | 100% | 100% | +0 pp |
| design | 100% | 100% | +0 pp |
| distributed-systems | 90% | 90% | +0 pp |
| ebpf | 100% | 100% | +0 pp |
| encoding | 100% | 100% | +0 pp |
| errors | 100% | 100% | +0 pp |
| event-driven | 100% | 20% | +80 pp |
| file-io | 100% | 100% | +0 pp |
| generics | 100% | 100% | +0 pp |
| internals | 100% | 100% | +0 pp |
| mcp-and-agents | 100% | 0% | +100 pp |
| modern | 100% | 0% | +100 pp |
| modernization | 98% | 44% | +53 pp |
| networking | 100% | 0% | +100 pp |
| observability | 100% | 100% | +0 pp |
| performance | 100% | 100% | +0 pp |
| security | 100% | 90% | +10 pp |
| wasm-and-embedded | 100% | 100% | +0 pp |
