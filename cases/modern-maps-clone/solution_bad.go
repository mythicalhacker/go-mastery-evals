package solution

// BUG: returns the input map directly. Maps are reference types, so the result
// is an alias of m, not a copy. Mutating the returned map mutates the original.
// A correct copy uses maps.Clone (or make + a range copy).
func Copy(m map[string]int) map[string]int {
	return m
}
