Implement, in Go, package `solution` (no `main` function):

A function `ReadConfig(path string) ([]byte, error)` that reads and returns the contents of the file at `path`. On failure it must return an error that adds context about what it was doing **and** preserves the underlying error so that callers can still match it with `errors.Is` (e.g. against `fs.ErrNotExist`).

Output only the Go code.
