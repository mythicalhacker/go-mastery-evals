Implement, in Go, package `solution` (no `main` function):

A function `Count(n int) iter.Seq[int]` that produces the integers `0, 1, …, n-1` in order, so it can be consumed with a range loop:

```go
for v := range Count(n) {
	// ...
}
```

The loop body may decide to stop early (with `break`) before reaching `n-1`; `Count` must behave correctly when the caller does so.

Use only the Go standard library. Output only the Go code.
