package solution

import (
	"runtime"
	"testing"
	"time"
)

// waitSettled returns true once the goroutine count falls back to ~base,
// polling up to d. Logic-based leak detection (no -race / C compiler needed).
func waitSettled(base int, d time.Duration) bool {
	deadline := time.Now().Add(d)
	for {
		runtime.GC()
		if runtime.NumGoroutine() <= base+2 {
			return true
		}
		if time.Now().After(deadline) {
			return runtime.NumGoroutine() <= base+2
		}
		time.Sleep(10 * time.Millisecond)
	}
}

func TestSearchAnyFindsMatch(t *testing.T) {
	v, ok := SearchAny([]int{1, 2, 3, 7, 4}, func(x int) bool { return x == 7 })
	if !ok || v != 7 {
		t.Fatalf("SearchAny = (%d, %v), want (7, true)", v, ok)
	}
}

func TestSearchAnyNoMatch(t *testing.T) {
	v, ok := SearchAny([]int{1, 2, 3}, func(int) bool { return false })
	if ok || v != 0 {
		t.Fatalf("SearchAny = (%d, %v), want (0, false)", v, ok)
	}
}

func TestSearchAnyNoLeak(t *testing.T) {
	base := runtime.NumGoroutine()
	// Every value matches: a naive unbuffered-send design returns the first match
	// and leaves the other senders blocked forever (no receiver) -> leak.
	values := make([]int, 20)
	for i := range values {
		values[i] = i + 1
	}
	v, ok := SearchAny(values, func(int) bool { return true })
	if !ok || v < 1 || v > 20 {
		t.Fatalf("SearchAny = (%d, %v), want a matching value", v, ok)
	}
	if !waitSettled(base, 2*time.Second) {
		t.Fatalf("goroutines leaked: base=%d, now=%d", base, runtime.NumGoroutine())
	}
}
