package solution

import (
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestLoadCoalescesConcurrentSameKey(t *testing.T) {
	var loader Loader
	var calls int64

	fetch := func() (int, error) {
		atomic.AddInt64(&calls, 1)
		time.Sleep(100 * time.Millisecond)
		return 7, nil
	}

	const n = 50
	start := make(chan struct{})
	results := make([]int, n)
	errs := make([]error, n)

	var wg sync.WaitGroup
	wg.Add(n)
	for i := 0; i < n; i++ {
		go func(idx int) {
			defer wg.Done()
			<-start
			v, err := loader.Load("k", fetch)
			results[idx] = v
			errs[idx] = err
		}(i)
	}

	close(start)
	wg.Wait()

	for i := 0; i < n; i++ {
		if errs[i] != nil {
			t.Fatalf("caller %d got error: %v", i, errs[i])
		}
		if results[i] != 7 {
			t.Fatalf("caller %d got %d, want 7", i, results[i])
		}
	}

	if got := atomic.LoadInt64(&calls); got != 1 {
		t.Fatalf("fetch ran %d times, want exactly 1 (concurrent same-key calls must coalesce)", got)
	}
}

func TestLoadDistinctKeysProceedIndependently(t *testing.T) {
	var loader Loader
	var calls int64

	makeFetch := func(ret int) func() (int, error) {
		return func() (int, error) {
			atomic.AddInt64(&calls, 1)
			return ret, nil
		}
	}

	v1, err := loader.Load("a", makeFetch(1))
	if err != nil || v1 != 1 {
		t.Fatalf("key a: got (%d, %v), want (1, nil)", v1, err)
	}
	v2, err := loader.Load("b", makeFetch(2))
	if err != nil || v2 != 2 {
		t.Fatalf("key b: got (%d, %v), want (2, nil)", v2, err)
	}

	if got := atomic.LoadInt64(&calls); got != 2 {
		t.Fatalf("fetch ran %d times for two distinct sequential keys, want 2", got)
	}
}
