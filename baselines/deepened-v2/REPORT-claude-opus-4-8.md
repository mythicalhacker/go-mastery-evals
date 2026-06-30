# Go Mastery — Eval Report

## Provenance

- **Model:** claude-opus-4-8
- **Runner:** anthropic
- **Temperature (applied):** not applied — model rejected the parameter
- **Samples / (case,variant):** 5
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:43293a4e71c8 (content)
- **Cases graded:** 54
- **Generated (UTC):** 2026-06-29 22:40:56Z

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
| concurrency-search-leak | concurrency | 5/5 | 5/5 |
| concurrency-select-done | concurrency | 5/5 | 5/5 |
| concurrency-worker-ctx | concurrency | 5/5 | 5/5 |
| correctness-concurrent-map | correctness | 5/5 | 5/5 |
| correctness-lost-update | correctness | 5/5 | 5/5 |
| correctness-parsesize | correctness | 5/5 | 5/5 |
| correctness-slice-aliasing | correctness | 5/5 | 5/5 |
| correctness-time-equal | correctness | 5/5 | 5/5 |
| database-valuer-scanner | database | 5/5 | 5/5 |
| datastructures-heap | data-structures | 5/5 | 5/5 |
| debugging-all-goroutine-stacks | debugging | 5/5 | 5/5 |
| design-iter-seq | design | 5/5 | 5/5 |
| distributed-consistent-hash | distributed-systems | 5/5 | 5/5 |
| ebpf-current-api | ebpf | 5/5 | 5/5 |
| encoding-json-number | encoding | 5/5 | 5/5 |
| encoding-varint | encoding | 5/5 | 5/5 |
| errors-join-aggregate | errors | 5/5 | 5/5 |
| errors-wrapping | errors | 5/5 | 5/5 |
| event-driven-bus | event-driven | 5/5 | 2/5 |
| file-io-os-root | file-io | 5/5 | 5/5 |
| frontier-errors-astype-2 | modernization | 5/5 | 0/5 |
| generics-filter | generics | 5/5 | 5/5 |
| grpc-interceptor-codes | distributed-systems | 5/5 | 5/5 |
| http-timeouts | api-design | 5/5 | 5/5 |
| internals-runtime-metrics | internals | 5/5 | 5/5 |
| mcp-current-sdk | mcp-and-agents | 5/5 | 5/5 |
| modern-clear-builtin | modern | 5/5 | 0/5 |
| modern-errors-astype | modernization | 5/5 | 0/5 |
| modern-maps-clone | data-structures | 5/5 | 5/5 |
| modern-maps-iter | modernization | 5/5 | 5/5 |
| modern-new-expr | modernization | 5/5 | 0/5 |
| modern-omitzero | modernization | 5/5 | 5/5 |
| modern-rand-v2 | modernization | 5/5 | 5/5 |
| modern-range-int | modernization | 5/5 | 5/5 |
| modern-slices-contains | modernization | 5/5 | 5/5 |
| modern-waitgroup-go | modernization | 5/5 | 5/5 |
| networking-netip | networking | 5/5 | 0/5 |
| niche-singleflight | concurrency | 5/5 | 5/5 |
| observability-otel-span | observability | 5/5 | 0/5 |
| observability-slog-redaction | observability | 5/5 | 5/5 |
| performance-pool-reset | performance | 5/5 | 5/5 |
| security-html-escaping | security | 5/5 | 5/5 |
| security-sql-injection | security | 5/5 | 5/5 |
| wasm-wasip1-build | wasm-and-embedded | 5/5 | 5/5 |

## Summary

- **with**: pass@1 100% (54/54 cases pass)
- **without**: pass@1 86% (46/54 cases pass)

- **Lift (pass@1, with − without): +14.1 pp**

## By category

| Category | with pass@1 | without pass@1 | lift |
|---|---|---|---|
| ai-ml-beyond-llm | 100% | 100% | +0 pp |
| api-design | 100% | 100% | +0 pp |
| cgo-and-interop | 100% | 100% | +0 pp |
| cli | 100% | 100% | +0 pp |
| cloud-native | 100% | 100% | +0 pp |
| concurrency | 100% | 89% | +11 pp |
| correctness | 100% | 100% | +0 pp |
| data-structures | 100% | 100% | +0 pp |
| database | 100% | 100% | +0 pp |
| debugging | 100% | 100% | +0 pp |
| design | 100% | 100% | +0 pp |
| distributed-systems | 100% | 100% | +0 pp |
| ebpf | 100% | 100% | +0 pp |
| encoding | 100% | 100% | +0 pp |
| errors | 100% | 100% | +0 pp |
| event-driven | 100% | 40% | +60 pp |
| file-io | 100% | 100% | +0 pp |
| generics | 100% | 100% | +0 pp |
| internals | 100% | 100% | +0 pp |
| mcp-and-agents | 100% | 100% | +0 pp |
| modern | 100% | 0% | +100 pp |
| modernization | 100% | 67% | +33 pp |
| networking | 100% | 0% | +100 pp |
| observability | 100% | 50% | +50 pp |
| performance | 100% | 100% | +0 pp |
| security | 100% | 100% | +0 pp |
| wasm-and-embedded | 100% | 100% | +0 pp |

## Quality by case (deterministic)

Idiom adoption − anti-patterns on comment-stripped code (per-case rubrics).

| Case | with | without | Δ | with: idioms present | with: idioms missing |
|---|---|---|---|---|---|
| ai-ml-gonum-stat | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-alphametics | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-beer-song | -0.3 | +0.0 | -0.3 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-book-store | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-bottle-song | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-bowling | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-connect | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-crypto-square | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-dnd-character | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-dominoes | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-error-handling | +0.0 | +0.0 | +0.0 | defer Close, anti:panic | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-food-chain | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-forth | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-hexadecimal | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-kindergarten-garden | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-matrix | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-octal | -0.3 | +0.0 | -0.3 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-paasio | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-palindrome-products | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-pig-latin | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-poker | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-pov | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-protein-translation | +1.0 | +1.0 | +0.0 | errors.Is/As | err %w, errors.Join, slog, slices/maps, cmp.Or, ctx param |
| aider-react | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-robot-simulator | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-say | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-scale-generator | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-simple-linked-list | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-sublist | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-transpose | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-tree-building | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-trinary | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-two-bucket | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-variable-length-quantity | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-word-search | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-wordy | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-zebra-puzzle | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| api-iter-ordered | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| cgo-c-interop | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| cli-flagset-subcommand | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| cloudnative-reconcile-configmap | +3.0 | +1.0 | +2.0 | err %w, slices/maps, ctx param | errors.Join, errors.Is/As, slog, cmp.Or, defer Close, once/wg.Go |
| concurrency-bounded-parallelism | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-deadline-propagation | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-detach-context | +2.0 | +1.0 | +1.0 | ctx param, WithoutCancel | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-oncevalues | +1.0 | +0.0 | +1.0 | once/wg.Go | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-pipeline-cancel | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-search-leak | +1.0 | +0.0 | +1.0 | once/wg.Go | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-select-done | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-worker-ctx | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| correctness-concurrent-map | +0.4 | +0.0 | +0.4 | once/wg.Go | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| correctness-json-number | +1.0 | +0.4 | +0.6 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| correctness-lost-update | +1.0 | +0.0 | +1.0 | once/wg.Go | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| correctness-parsesize | +1.0 | +0.2 | +0.8 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| correctness-slice-aliasing | +0.2 | +0.0 | +0.2 | slices/maps | err %w, errors.Join, errors.Is/As, slog, cmp.Or, ctx param |
| correctness-time-equal | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| database-valuer-scanner | +0.0 | -1.0 | +1.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| datastructures-heap | +0.0 | -1.0 | +1.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| debugging-all-goroutine-stacks | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| design-iter-seq | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| distributed-consistent-hash | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| ebpf-current-api | +1.0 | +0.0 | +1.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| encoding-json-number | +1.0 | +1.0 | +0.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| encoding-varint | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| errors-join-aggregate | +1.0 | +1.8 | -0.8 | errors.Join | err %w, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| errors-wrapping | +1.0 | +1.0 | +0.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| event-driven-bus | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| file-io-os-root | +1.0 | +0.4 | +0.6 | defer Close | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| frontier-errors-astype-2 | +1.0 | +1.0 | +0.0 | errors.Is/As | err %w, errors.Join, slog, slices/maps, cmp.Or, ctx param |
| frontier-weak-cache | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| generics-filter | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| grpc-interceptor-codes | +2.0 | +1.0 | +1.0 | errors.Is/As, ctx param | err %w, errors.Join, slog, slices/maps, cmp.Or, defer Close |
| http-timeouts | +3.0 | +3.0 | +0.0 | ReadTimeout, WriteTimeout, ReadHeaderTimeout | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| internals-runtime-metrics | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| io-osroot | +1.2 | +1.0 | +0.2 | defer Close | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| mcp-current-sdk | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-clear-builtin | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-errors-astype | +1.0 | +1.0 | +0.0 | errors.Is/As | err %w, errors.Join, slog, slices/maps, cmp.Or, ctx param |
| modern-maps-clone | +1.0 | +0.0 | +1.0 | slices/maps | err %w, errors.Join, errors.Is/As, slog, cmp.Or, ctx param |
| modern-maps-iter | +1.0 | +1.0 | +0.0 | slices/maps | err %w, errors.Join, errors.Is/As, slog, cmp.Or, ctx param |
| modern-new-expr | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-omitzero | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-rand-v2 | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-range-int | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-slices-contains | +1.0 | +1.0 | +0.0 | slices/maps | err %w, errors.Join, errors.Is/As, slog, cmp.Or, ctx param |
| modern-waitgroup-go | +1.0 | +1.0 | +0.0 | once/wg.Go | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| networking-netip | +1.0 | +1.0 | +0.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| niche-singleflight | +0.0 | -0.8 | +0.8 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| observability-otel-span | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| observability-slog-redaction | +1.0 | +1.0 | +0.0 | slog | err %w, errors.Join, errors.Is/As, slices/maps, cmp.Or, ctx param |
| performance-pool-reset | +0.0 | -1.0 | +1.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| security-html-escaping | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| security-sql-injection | +4.0 | +2.2 | +1.8 | err %w, errors.Is/As, ctx param, placeholder $N | errors.Join, slog, slices/maps, cmp.Or, defer Close, once/wg.Go |
| wasm-wasip1-build | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
