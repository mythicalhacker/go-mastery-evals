Implement, in Go, package `solution` (no `main` function):

1. A `NotFound` error type with an exported `Key string` field that implements the `error` interface.
2. A function `Lookup(err error) (string, bool)` that reports whether `err` is, or wraps, a `*NotFound`. If so, return its `Key` and `true`; otherwise return `"", false`.

Use the most modern Go idiom available for typed error extraction. Output only the Go code.
