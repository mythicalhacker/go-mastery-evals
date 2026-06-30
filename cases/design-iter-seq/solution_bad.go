package solution

import "iter"

// BUG: ignores the bool returned by yield. When the consumer breaks early,
// yield returns false, but this keeps calling yield afterward. The runtime
// detects a yield call after it returned false and panics. Correct code
// returns as soon as yield reports false.
func Count(n int) iter.Seq[int] {
	return func(yield func(int) bool) {
		for i := 0; i < n; i++ {
			yield(i)
		}
	}
}
