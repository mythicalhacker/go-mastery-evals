package solution

import "sync"

// Memoize returns a function that runs load at most once and caches its
// (value, error) result, returning the same pair to every caller even under
// concurrent access. sync.OnceValues handles the once-and-share semantics.
func Memoize(load func() (int, error)) func() (int, error) {
	return sync.OnceValues(load)
}
