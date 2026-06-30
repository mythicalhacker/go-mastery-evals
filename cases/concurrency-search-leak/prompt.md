Implement, in Go, package `solution` (no `main` function):

A function `SearchAny(values []int, match func(int) bool) (int, bool)` that returns a value from `values` for which `match` returns true, together with `true`; or `(0, false)` if no value matches.

Evaluate the `match` calls concurrently — one goroutine per value — and return as soon as the first match is found, without waiting for the remaining calls. The function must not leak goroutines: by the time it returns, for any input, every goroutine it started must have finished or be guaranteed to finish on its own (no goroutine may be left blocked forever).

Use only the Go standard library. Output only the Go code.
