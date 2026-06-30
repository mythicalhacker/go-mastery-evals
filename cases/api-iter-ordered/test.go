package solution

import (
	"slices"
	"testing"
)

func TestCounterAllSortedOrder(t *testing.T) {
	var c Counter
	// Add keys out of order, with one repeated key.
	for _, k := range []string{"d", "b", "a", "c", "a", "g", "e", "f"} {
		c.Add(k)
	}

	var keys []string
	counts := map[string]int{}
	for k, n := range c.All() {
		keys = append(keys, k)
		counts[k] = n
	}

	wantKeys := []string{"a", "b", "c", "d", "e", "f", "g"}
	if !slices.Equal(keys, wantKeys) {
		t.Fatalf("All() visited keys in order %v, want ascending %v", keys, wantKeys)
	}

	wantCounts := map[string]int{"a": 2, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1}
	for k, want := range wantCounts {
		if counts[k] != want {
			t.Fatalf("count for %q = %d, want %d", k, counts[k], want)
		}
	}
}

func TestCounterAllEarlyBreak(t *testing.T) {
	var c Counter
	for _, k := range []string{"z", "y", "x"} {
		c.Add(k)
	}

	var first string
	for k := range c.All() {
		first = k
		break // must be honored; first key in ascending order is "x"
	}
	if first != "x" {
		t.Fatalf("first yielded key = %q, want %q", first, "x")
	}
}
