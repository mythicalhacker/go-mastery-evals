Implement, in Go, package `solution` (no `main` function):

A single reusable function `Filter` that returns the elements of a slice for which a predicate returns true, preserving their original order.

It must work for **any** element type with no per-type duplication and without losing static typing: callers should be able to use it directly on a `[]int` and on a `[]string` and get back a `[]int` and a `[]string` respectively, with no type assertions or conversions at the call site.

Use only the Go standard library. Output only the Go code.
