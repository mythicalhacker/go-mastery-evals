package solution

// BUG: when items has spare capacity, append writes the new element into the
// caller's backing array, mutating data the caller can still observe (aliasing).
func AppendTag(items []string, tag string) []string {
	return append(items, tag)
}
