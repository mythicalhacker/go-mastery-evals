package solution

// BUG: the cache has no synchronization. Under concurrent calls multiple
// goroutines see done == false at the same time and each runs load, so load
// runs more than once (and the reads/writes of done/val/err are a data race).
// Correct code memoizes with sync.OnceValues so load runs exactly once.
func Memoize(load func() (int, error)) func() (int, error) {
	var done bool
	var val int
	var err error
	return func() (int, error) {
		if !done {
			val, err = load()
			done = true
		}
		return val, err
	}
}
