package solution

import (
	"errors"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func TestMemoizeRunsOnceUnderConcurrency(t *testing.T) {
	var calls int64
	sentinel := errors.New("boom")
	load := func() (int, error) {
		// Sleep before bumping the counter so unsynchronized callers overlap
		// inside load and the race is observable rather than timing-dependent.
		time.Sleep(20 * time.Millisecond)
		atomic.AddInt64(&calls, 1)
		return 42, sentinel
	}

	m := Memoize(load)

	const goroutines = 50
	var wg sync.WaitGroup
	vals := make([]int, goroutines)
	errs := make([]error, goroutines)
	wg.Add(goroutines)
	for i := range goroutines {
		go func() {
			defer wg.Done()
			vals[i], errs[i] = m()
		}()
	}
	wg.Wait()

	if n := atomic.LoadInt64(&calls); n != 1 {
		t.Fatalf("load ran %d times, want exactly 1", n)
	}
	for i := range goroutines {
		if vals[i] != 42 {
			t.Fatalf("caller %d got value %d, want 42", i, vals[i])
		}
		if !errors.Is(errs[i], sentinel) {
			t.Fatalf("caller %d got error %v, want %v", i, errs[i], sentinel)
		}
	}
}

func TestMemoizeCachesAcrossSequentialCalls(t *testing.T) {
	var calls int64
	load := func() (int, error) {
		atomic.AddInt64(&calls, 1)
		return 7, nil
	}
	m := Memoize(load)

	for i := 0; i < 5; i++ {
		v, err := m()
		if v != 7 || err != nil {
			t.Fatalf("call %d = (%d, %v), want (7, nil)", i, v, err)
		}
	}
	if n := atomic.LoadInt64(&calls); n != 1 {
		t.Fatalf("load ran %d times across repeated calls, want exactly 1", n)
	}
}
