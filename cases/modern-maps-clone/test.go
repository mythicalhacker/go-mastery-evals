package solution

import "testing"

func TestCopyIsIndependent(t *testing.T) {
	orig := map[string]int{"a": 1}
	c := Copy(orig)

	// Mutate the copy: change an existing key and add a new one.
	c["a"] = 99
	c["b"] = 2

	// The original must be untouched by mutations to the copy.
	if orig["a"] != 1 {
		t.Fatalf("orig[\"a\"] = %d, want 1 (copy mutation leaked into original)", orig["a"])
	}
	if _, ok := orig["b"]; ok {
		t.Fatalf("orig gained key \"b\"; copy is an alias, not an independent copy")
	}

	// The copy must actually reflect the caller's mutations.
	if c["a"] != 99 {
		t.Fatalf("c[\"a\"] = %d, want 99", c["a"])
	}
}
