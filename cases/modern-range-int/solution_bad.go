package solution

// BUG: C-style index loop instead of the modern range-over-integer form.
func FirstN(n int) []int {
	var out []int
	for i := 0; i < n; i++ {
		out = append(out, i)
	}
	return out
}
