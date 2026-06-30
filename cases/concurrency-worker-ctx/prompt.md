Implement, in Go, package `solution` (no `main` function):

A function `Run(ctx context.Context, jobs <-chan int) <-chan int` that starts a single worker which reads integers from `jobs`, doubles each one, and sends the result on the returned channel. The worker must exit cleanly — closing the returned channel — when either `jobs` is closed or `ctx` is cancelled. It must not leak a goroutine and must not block forever on send when the context is cancelled.

Output only the Go code.
