Implement, in Go, package `solution` (no `main` function):

A function `Memoize(load func() (int, error)) func() (int, error)` that memoizes an expensive initializer.

The returned function caches the result of calling `load` (both the value and the error) and returns it to every caller. `load` must run at most once, even when the returned function is called concurrently from many goroutines, and all callers must observe the same value and the same error.

Use only the Go standard library. Output only the Go code.
