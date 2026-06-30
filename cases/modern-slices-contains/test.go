package solution

import "testing"

func TestContains(t *testing.T) {
	xs := []string{"a", "b", "c"}
	if !Contains(xs, "b") {
		t.Fatal("Contains(xs, b) = false, want true")
	}
	if Contains(xs, "z") {
		t.Fatal("Contains(xs, z) = true, want false")
	}
}
