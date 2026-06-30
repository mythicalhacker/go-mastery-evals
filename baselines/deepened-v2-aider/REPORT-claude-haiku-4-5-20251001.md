# Go Mastery — Eval Report

## Provenance

- **Model:** claude-haiku-4-5-20251001
- **Runner:** anthropic
- **Temperature (applied):** 0.0
- **Samples / (case,variant):** 3
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:43293a4e71c8 (content)
- **Cases graded:** 36
- **Generated (UTC):** 2026-06-30 00:39:22Z

## Per-case results (passes / samples)

| Case | Category | with | without |
|---|---|---|---|
| aider-alphametics | aider-polyglot | 0/3 | 0/3 |
| aider-beer-song | aider-polyglot | 0/3 | 0/3 |
| aider-book-store | aider-polyglot | 0/3 | 0/3 |
| aider-bottle-song | aider-polyglot | 0/3 | 0/3 |
| aider-bowling | aider-polyglot | 0/3 | 0/3 |
| aider-connect | aider-polyglot | 0/3 | 0/3 |
| aider-crypto-square | aider-polyglot | 3/3 | 3/3 |
| aider-dnd-character | aider-polyglot | 0/3 | 0/3 |
| aider-dominoes | aider-polyglot | 1/3 | 0/3 |
| aider-error-handling | aider-polyglot | 0/3 | 0/3 |
| aider-food-chain | aider-polyglot | 1/3 | 1/3 |
| aider-forth | aider-polyglot | 0/3 | 0/3 |
| aider-hexadecimal | aider-polyglot | 0/3 | 0/3 |
| aider-kindergarten-garden | aider-polyglot | 0/3 | 0/3 |
| aider-matrix | aider-polyglot | 0/3 | 0/3 |
| aider-octal | aider-polyglot | 0/3 | 0/3 |
| aider-paasio | aider-polyglot | 3/3 | 0/3 |
| aider-palindrome-products | aider-polyglot | 0/3 | 0/3 |
| aider-pig-latin | aider-polyglot | 3/3 | 3/3 |
| aider-poker | aider-polyglot | 0/3 | 0/3 |
| aider-pov | aider-polyglot | 0/3 | 0/3 |
| aider-protein-translation | aider-polyglot | 0/3 | 0/3 |
| aider-react | aider-polyglot | 0/3 | 0/3 |
| aider-robot-simulator | aider-polyglot | 0/3 | 0/3 |
| aider-say | aider-polyglot | 2/3 | 3/3 |
| aider-scale-generator | aider-polyglot | 0/3 | 0/3 |
| aider-simple-linked-list | aider-polyglot | 0/3 | 0/3 |
| aider-sublist | aider-polyglot | 0/3 | 0/3 |
| aider-transpose | aider-polyglot | 0/3 | 0/3 |
| aider-tree-building | aider-polyglot | 0/3 | 0/3 |
| aider-trinary | aider-polyglot | 0/3 | 0/3 |
| aider-two-bucket | aider-polyglot | 2/3 | 0/3 |
| aider-variable-length-quantity | aider-polyglot | 0/3 | 3/3 |
| aider-word-search | aider-polyglot | 0/3 | 0/3 |
| aider-wordy | aider-polyglot | 0/3 | 0/3 |
| aider-zebra-puzzle | aider-polyglot | 0/3 | 0/3 |

## Summary

- **with**: pass@1 14% (5/36 cases pass)
- **without**: pass@1 12% (4/36 cases pass)

- **Lift (pass@1, with − without): +1.9 pp**

## By category

| Category | with pass@1 | without pass@1 | lift |
|---|---|---|---|
| aider-polyglot | 14% | 12% | +2 pp |

## Quality by case (deterministic)

Idiom adoption − anti-patterns on comment-stripped code (per-case rubrics).

| Case | with | without | Δ | with: idioms present | with: idioms missing |
|---|---|---|---|---|---|
| ai-ml-gonum-stat | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-alphametics | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-beer-song | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-book-store | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-bottle-song | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-bowling | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-connect | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-crypto-square | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-dnd-character | +1.0 | +0.0 | +1.0 | slices/maps | err %w, errors.Join, errors.Is/As, slog, cmp.Or, ctx param |
| aider-dominoes | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-error-handling | +0.0 | +0.0 | +0.0 | defer Close, anti:panic | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-food-chain | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-forth | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-hexadecimal | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-kindergarten-garden | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-matrix | +1.0 | +0.0 | +1.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| aider-octal | -1.0 | -1.0 | +0.0 | anti:panic | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-paasio | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-palindrome-products | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-pig-latin | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-poker | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-pov | -1.0 | +0.0 | -1.0 | anti:panic | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| aider-protein-translation | +1.0 | +0.0 | +1.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| aider-react | -0.3 | -1.0 | +0.7 | anti:panic | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
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
| cli-flagset-subcommand | +1.0 | +0.8 | +0.2 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| cloudnative-reconcile-configmap | +2.0 | +2.0 | +0.0 | err %w, ctx param | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, defer Close |
| concurrency-bounded-parallelism | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-deadline-propagation | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-detach-context | +0.0 | +0.0 | +0.0 | ctx param, anti:interface{} | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-oncevalues | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-pipeline-cancel | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-search-leak | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-select-done | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| concurrency-worker-ctx | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| correctness-concurrent-map | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| correctness-json-number | +1.0 | -1.0 | +2.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| correctness-lost-update | +1.0 | +0.0 | +1.0 | once/wg.Go | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| correctness-parsesize | +1.0 | +0.0 | +1.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| correctness-slice-aliasing | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| correctness-time-equal | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| database-valuer-scanner | +0.0 | -1.0 | +1.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| datastructures-heap | +0.0 | -1.0 | +1.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| debugging-all-goroutine-stacks | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| design-iter-seq | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| distributed-consistent-hash | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| ebpf-current-api | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| encoding-json-number | +1.0 | +1.0 | +0.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| encoding-varint | +1.0 | +0.0 | +1.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| errors-join-aggregate | +1.0 | +1.0 | +0.0 | errors.Join | err %w, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| errors-wrapping | +1.0 | +1.0 | +0.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| event-driven-bus | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| file-io-os-root | +2.0 | +1.0 | +1.0 | err %w, defer Close | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| frontier-errors-astype-2 | +1.0 | +1.0 | +0.0 | errors.Is/As | err %w, errors.Join, slog, slices/maps, cmp.Or, ctx param |
| frontier-weak-cache | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| generics-filter | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| grpc-interceptor-codes | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| http-timeouts | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| internals-runtime-metrics | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| io-osroot | +1.0 | +0.2 | +0.8 | defer Close | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| mcp-current-sdk | +1.0 | -0.2 | +1.2 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-clear-builtin | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-errors-astype | +1.0 | +1.0 | +0.0 | errors.Is/As | err %w, errors.Join, slog, slices/maps, cmp.Or, ctx param |
| modern-maps-clone | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-maps-iter | +1.0 | +1.0 | +0.0 | slices/maps | err %w, errors.Join, errors.Is/As, slog, cmp.Or, ctx param |
| modern-new-expr | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-omitzero | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-rand-v2 | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-range-int | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| modern-slices-contains | +1.0 | +1.0 | +0.0 | slices/maps | err %w, errors.Join, errors.Is/As, slog, cmp.Or, ctx param |
| modern-waitgroup-go | +1.0 | +0.0 | +1.0 | once/wg.Go | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| networking-netip | +1.0 | +1.0 | +0.0 | err %w | errors.Join, errors.Is/As, slog, slices/maps, cmp.Or, ctx param |
| niche-singleflight | +0.0 | -1.0 | +1.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| observability-otel-span | +1.0 | +1.0 | +0.0 | ctx param | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| observability-slog-redaction | +1.0 | +1.0 | +0.0 | slog | err %w, errors.Join, errors.Is/As, slices/maps, cmp.Or, ctx param |
| performance-pool-reset | +0.0 | -1.0 | +1.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| security-html-escaping | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
| security-sql-injection | +3.0 | +1.0 | +2.0 | err %w, errors.Is/As, ctx param | errors.Join, slog, slices/maps, cmp.Or, defer Close, once/wg.Go |
| wasm-wasip1-build | +0.0 | +0.0 | +0.0 |  | err %w, errors.Join, errors.Is/As, slog, slices/maps, cmp.Or |
