package solution

import "time"

// BUG: == compares the struct fields — wall-clock encoding, monotonic reading,
// and the *Location pointer — so two values for the same instant in different
// zones compare unequal. The same-moment comparison must ignore location.
func SameInstant(a, b time.Time) bool {
	return a == b
}
