package solution

// BUG: reassigns the local parameter to a fresh map. A map argument is the
// header passed by value, so this only rebinds the copy; the caller's map is
// untouched and still holds its entries. Emptying the existing map (clear)
// would mutate what the caller still references.
func Reset(m map[string]int) {
	m = make(map[string]int)
	_ = m
}
