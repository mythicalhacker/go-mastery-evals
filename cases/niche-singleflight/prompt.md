# Coalescing concurrent lookups

Implement a `Loader` type with the following method:

```go
func (l *Loader) Load(key string, fetch func() (int, error)) (int, error)
```

Contract:

- When multiple goroutines call `Load` with the **same** `key` at the same
  time, the supplied `fetch` function must execute **at most once**, and every
  one of those concurrent callers must receive that single shared result (value
  and error).
- Calls for **different** keys proceed independently of one another.
- A `Loader` value must be usable for many `Load` calls over its lifetime.
- If `fetch` returns an error, that error is propagated to the caller(s).

Provide the most modern, idiomatic Go implementation. Put your code in package
`solution` in `solution.go`. You may use the standard library and the vendored
`golang.org/x/sync` module.
