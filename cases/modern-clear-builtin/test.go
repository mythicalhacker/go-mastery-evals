package solution

import "testing"

func TestResetEmptiesCallersMap(t *testing.T) {
	m := map[string]int{"a": 1, "b": 2}
	ref := m // keep a reference to the very same map instance

	Reset(m)

	if len(m) != 0 {
		t.Fatalf("caller's map not emptied: len = %d, want 0", len(m))
	}
	// The caller's reference must observe the change on the SAME instance.
	// A version that reassigns a fresh local map leaves this at len 2.
	if len(ref) != 0 {
		t.Fatalf("original map instance still populated: len = %d, want 0", len(ref))
	}
}
