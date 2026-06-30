Implement, in Go, package `solution` (no `main` function):

A function `MapConcurrent(items []int, limit int, f func(int) int) []int` that applies `f` to every item concurrently and returns the results in the same order as `items`.

At most `limit` invocations of `f` may run at the same time (assume `limit >= 1`). Process the items concurrently up to that bound — do not run them all at once, and do not fall back to running them one at a time.

Use only the Go standard library. Output only the Go code.
