Implement, in Go, package `solution` (no `main` function):

A function `SumCounter(workers, increments int) int64` that starts `workers` goroutines, each of which increments a single shared counter `increments` times. After all goroutines finish, return the counter's value.

The returned total must always equal `workers * increments`, no matter how the goroutines interleave.

Use only the Go standard library. Output only the Go code.
