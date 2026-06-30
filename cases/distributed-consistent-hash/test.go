package solution

import (
	"fmt"
	"testing"
)

func TestConsistentHashMinimalDisruption(t *testing.T) {
	nodes := make([]string, 10)
	for i := range nodes {
		nodes[i] = fmt.Sprintf("n%d", i)
	}
	r := NewRing(nodes...)

	const numKeys = 2000
	keys := make([]string, numKeys)
	before := make(map[string]string, numKeys)
	for i := range keys {
		k := fmt.Sprintf("key-%d", i)
		keys[i] = k
		n := r.Get(k)
		if n == "" {
			t.Fatalf("Get(%q) returned empty node before removal", k)
		}
		before[k] = n
	}

	const removed = "n5"
	r.Remove(removed)

	present := make(map[string]bool, len(nodes)-1)
	for _, n := range nodes {
		if n != removed {
			present[n] = true
		}
	}

	var eligible, moved int
	for _, k := range keys {
		now := r.Get(k)
		if now == "" {
			t.Fatalf("Get(%q) returned empty node after removal", k)
		}
		if !present[now] {
			t.Fatalf("Get(%q) returned %q which is not a currently-present node", k, now)
		}
		if before[k] == removed {
			continue // the removed node's keys are expected to move
		}
		eligible++
		if now != before[k] {
			moved++
		}
	}

	if eligible == 0 {
		t.Fatal("no keys were eligible; test setup is broken")
	}
	frac := float64(moved) / float64(eligible)
	if frac >= 0.05 {
		t.Fatalf("minimal disruption violated: %d/%d (%.1f%%) of keys not on the removed node changed owners; want < 5%%",
			moved, eligible, frac*100)
	}
}
