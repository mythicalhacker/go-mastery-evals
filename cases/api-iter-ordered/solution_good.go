package solution

import (
	"iter"
	"slices"
)

type Counter struct {
	counts map[string]int
}

func (c *Counter) Add(key string) {
	if c.counts == nil {
		c.counts = make(map[string]int)
	}
	c.counts[key]++
}

// All returns a sequence over (key, count) pairs in ascending key order.
// The internal map is never exposed; callers only receive copied values.
func (c *Counter) All() iter.Seq2[string, int] {
	return func(yield func(string, int) bool) {
		keys := make([]string, 0, len(c.counts))
		for k := range c.counts {
			keys = append(keys, k)
		}
		slices.Sort(keys)
		for _, k := range keys {
			if !yield(k, c.counts[k]) {
				return
			}
		}
	}
}
