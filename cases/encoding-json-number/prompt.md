Implement, in Go, package `solution` (no `main` function):

A function `ParseID(data []byte) (int64, error)` that decodes a JSON object of the form `{"id":9007199254740993}` and returns the value of its `id` field as an `int64`.

The `id` is a large integer that must be returned exactly, with no rounding or loss of precision. On malformed input, return a non-nil error.

Use only the Go standard library. Output only the Go code.
