Implement, in Go, package `solution` (no `main` function):

A function `Fetch(ctx context.Context, source func(context.Context) (int, error)) (int, error)` that obtains a value by calling the downstream `source` function and returns its result and error unchanged.

The caller may impose a deadline or cancellation through `ctx`. `Fetch` must ensure the downstream `source` call observes that same deadline/cancellation — if `ctx` is cancelled or times out, `source` must see it and be able to stop, rather than running unbounded.

Use only the Go standard library. Output only the Go code.
