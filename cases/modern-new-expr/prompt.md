# Pointer fields from values

Define the following type, representing optional configuration where the
absence of a value must be distinguishable from a zero value:

```go
type Settings struct {
    Retries *int
    Label   *string
}
```

Implement:

```go
func NewSettings(retries int, label string) *Settings
```

Contract:

- The returned `*Settings` must be non-nil, with both `Retries` and `Label`
  pointing to allocated values.
- `*result.Retries` must equal the `retries` argument and `*result.Label`
  must equal the `label` argument.
- Each pointed-to value must be an **independent copy**: mutating the
  caller's original `retries`/`label` variables after the call must not
  change the values inside the returned struct, and two separate calls must
  return distinct pointers.

Use the most modern, idiomatic Go approach for allocating a pointer to a
copy of a value. Put your code in `solution.go`, package `solution`.
