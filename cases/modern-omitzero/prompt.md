Implement, in Go, package `solution` (no `main` function):

1. A struct type `Event` with two fields: `Name string` and `When time.Time`.
2. A function `Marshal(e Event) ([]byte, error)` that returns the JSON encoding of `e`, using the JSON keys `name` and `when`.

The JSON must omit the `when` field entirely when `When` holds the zero `time.Time` value, while still including it when it is set. Use the most modern standard-library struct-tag option that correctly handles this. Use only the Go standard library. Output only the Go code.
