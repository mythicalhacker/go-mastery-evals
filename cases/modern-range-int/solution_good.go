package solution

func FirstN(n int) []int {
	var out []int
	for i := range n {
		out = append(out, i)
	}
	return out
}
