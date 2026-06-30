package solution

import (
	"maps"
	"testing"
)

func TestCountConcurrentCorrect(t *testing.T) {
	got := CountConcurrent([]int{1, 1, 2, 3, 3, 3}, 4)
	want := map[int]int{1: 2, 2: 1, 3: 3}
	if !maps.Equal(got, want) {
		t.Fatalf("CountConcurrent = %v, want %v", got, want)
	}
}

func TestCountConcurrentSharded(t *testing.T) {
	// Large, sharded workload. An unsynchronized shared map fails one of two
	// ways: the runtime "concurrent map writes" panic, or — if it dodges that —
	// lost updates that make the exact counts below wrong. A correct version
	// (per-worker maps, or a guarded shared map) passes deterministically.
	const n, distinct = 100000, 500
	values := make([]int, n)
	for i := range values {
		values[i] = i % distinct
	}
	got := CountConcurrent(values, 8)
	if len(got) != distinct {
		t.Fatalf("got %d distinct keys, want %d", len(got), distinct)
	}
	for k, c := range got {
		if c != n/distinct {
			t.Fatalf("count[%d] = %d, want %d", k, c, n/distinct)
		}
	}
}
