Implement, in Go, package `solution` (no `main` function):

A function `Detach(ctx context.Context) context.Context` for starting background work that must outlive an inbound request. The returned context must:
- still expose every value carried by `ctx`; but
- NOT be cancelled (and its `Done()` must not fire) when `ctx` is cancelled.

Output only the Go code.
