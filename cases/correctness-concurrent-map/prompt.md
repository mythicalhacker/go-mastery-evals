Implement, in Go, package `solution` (no `main` function):

A function `CountConcurrent(values []int, workers int) map[int]int` that counts how many times each value appears in `values`, distributing the work across `workers` goroutines that run in parallel (assume `workers >= 1`).

Return a map from each distinct value to its total count. The result must be correct regardless of how the work is scheduled across the goroutines.

Use only the Go standard library. Output only the Go code.
