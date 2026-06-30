Implement, in Go, package `solution` (no `main` function):

1. An error type `RateLimited` with an exported integer field `RetryAfterSeconds`. It must implement the `error` interface using a value receiver (not a pointer receiver).
2. A function `RetryAfter(err error) (int, bool)` that reports whether `err` is, or wraps anywhere in its chain, a `RateLimited`. If so, return its `RetryAfterSeconds` and `true`; otherwise return `0, false`. The error may be wrapped through several layers (for example `fmt.Errorf("outer: %w", fmt.Errorf("mid: %w", RateLimited{...}))`).

Use the most modern Go idiom available for typed error extraction. Output only the Go code.
