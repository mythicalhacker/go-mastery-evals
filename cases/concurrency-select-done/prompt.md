Implement, in Go, package `solution` (no `main` function):

A function `Merge(ctx context.Context, a, b <-chan int) (int, bool)` that returns the first value available from either `a` or `b`, together with `true`. If `ctx` is cancelled before any value arrives on either channel, it must return `(0, false)` promptly instead of continuing to wait.

Use only the Go standard library. Output only the Go code.
