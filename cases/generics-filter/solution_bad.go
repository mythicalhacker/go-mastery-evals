package solution

// BUG: not generic. Hardcoding []any forces every caller to box their elements
// and breaks static typing, so the typed call sites Filter([]int{...}, ...) and
// Filter([]string{...}, ...) do not type-check against this signature. Correct
// code parameterizes over the element type with a type parameter.
func Filter(s []any, keep func(any) bool) []any {
	out := make([]any, 0)
	for _, v := range s {
		if keep(v) {
			out = append(out, v)
		}
	}
	return out
}
