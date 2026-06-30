package solution

import (
	"sync/atomic"
	"testing"
	"time"
)

func TestMapConcurrentOrderAndValues(t *testing.T) {
	items := []int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	got := MapConcurrent(items, 3, func(x int) int { return x * x })
	for i, v := range items {
		if got[i] != v*v {
			t.Fatalf("got[%d] = %d, want %d", i, got[i], v*v)
		}
	}
}

func TestMapConcurrentRespectsLimit(t *testing.T) {
	const limit = 3
	var cur, max int64
	f := func(x int) int {
		n := atomic.AddInt64(&cur, 1)
		for { // track the high-water mark of concurrent calls
			m := atomic.LoadInt64(&max)
			if n <= m || atomic.CompareAndSwapInt64(&max, m, n) {
				break
			}
		}
		time.Sleep(15 * time.Millisecond) // hold the slot so overlap is observable
		atomic.AddInt64(&cur, -1)
		return x
	}
	items := make([]int, 30)
	for i := range items {
		items[i] = i
	}
	MapConcurrent(items, limit, f)
	if m := atomic.LoadInt64(&max); m > limit {
		t.Fatalf("observed %d concurrent calls, limit was %d", m, limit)
	}
	if m := atomic.LoadInt64(&max); m < 2 {
		t.Fatalf("observed max concurrency %d; work did not actually run concurrently", m)
	}
}
