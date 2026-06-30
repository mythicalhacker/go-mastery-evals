package solution

import "iter"

type Counter struct {
	counts map[string]int
}

func (c *Counter) Add(key string) {
	if c.counts == nil {
		c.counts = make(map[string]int)
	}
	c.counts[key]++
}

// BUG: ranges the internal map directly, so pairs are yielded in Go's
// randomized map-iteration order rather than ascending key order. Correct
// code collects the keys, sorts them, and yields in that order.
func (c *Counter) All() iter.Seq2[string, int] {
	return func(yield func(string, int) bool) {
		for k, n := range c.counts {
			if !yield(k, n) {
				return
			}
		}
	}
}
