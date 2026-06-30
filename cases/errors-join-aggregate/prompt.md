Implement, in Go, package `solution` (no `main` function):

Two exported sentinel errors `ErrEmptyName` and `ErrNegativeAge`, and a function `Validate(name string, age int) error` that validates its inputs:
- if `name` is empty, that is an `ErrEmptyName` failure;
- if `age` is negative, that is an `ErrNegativeAge` failure.

If BOTH inputs are invalid, the returned error must let a caller detect BOTH failures with `errors.Is` (against each sentinel). If only one is invalid, only that one must match. If both are valid, return `nil`.

Output only the Go code.
