package solution

// BUG: behaviorally correct but hand-rolls the loop instead of using the
// stdlib membership helper the case asks for.
func Contains(xs []string, x string) bool {
	for _, v := range xs {
		if v == x {
			return true
		}
	}
	return false
}
