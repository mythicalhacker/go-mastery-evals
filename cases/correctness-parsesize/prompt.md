Implement, in Go, package `solution` (no `main` function):

A function `ParseSize(s string) (int64, error)` that parses a human-readable size into a number of bytes:

- Suffix `B` = bytes, `KB` = 1024 bytes, `MB` = 1024*1024 bytes (e.g. `"100B"` -> 100, `"2KB"` -> 2048, `"1MB"` -> 1048576).
- An empty string or any malformed input returns a non-nil error.

Output only the Go code.
