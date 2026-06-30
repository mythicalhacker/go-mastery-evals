Implement, in Go, package `solution` (no `main` function):

A function `ProcessAll(items []int, f func(int))` that invokes `f` on every item concurrently (one goroutine per item) and returns only after all invocations have completed.

Use the most modern `sync.WaitGroup` idiom available. Output only the Go code.
