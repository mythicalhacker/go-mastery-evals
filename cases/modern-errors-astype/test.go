package solution

import (
	"fmt"
	"testing"
)

func TestLookupFound(t *testing.T) {
	wrapped := fmt.Errorf("context: %w", &NotFound{Key: "k1"})
	key, ok := Lookup(wrapped)
	if !ok || key != "k1" {
		t.Fatalf("Lookup = (%q, %v), want (k1, true)", key, ok)
	}
}

func TestLookupNotFound(t *testing.T) {
	if _, ok := Lookup(fmt.Errorf("unrelated")); ok {
		t.Fatalf("Lookup on unrelated error = true, want false")
	}
}
