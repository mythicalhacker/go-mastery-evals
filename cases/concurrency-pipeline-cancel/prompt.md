Implement, in Go, package `solution` (no `main` function):

A function `Squares(ctx context.Context, nums []int) <-chan int` that builds a concurrent, multi-stage pipeline: one stage emits each value from `nums`, and a second stage squares it. The squared values are sent, in order, on the returned channel.

The returned channel must be closed once all values have been processed. If `ctx` is cancelled before the consumer has read everything, every stage must stop promptly and the function must leak no goroutines — even if the consumer stops reading after cancelling.

Use only the Go standard library. Output only the Go code.
