package solution

import (
	"slices"
	"testing"
)

func TestAppendTagResult(t *testing.T) {
	got := AppendTag([]string{"a", "b"}, "c")
	if !slices.Equal(got, []string{"a", "b", "c"}) {
		t.Fatalf("AppendTag = %v, want [a b c]", got)
	}
}

func TestAppendTagNoAliasing(t *testing.T) {
	backing := make([]string, 3, 10) // len 3, cap 10
	backing[0], backing[1], backing[2] = "a", "b", "c"
	items := backing[:2] // len 2, shares the backing array (index 2 holds "c")

	_ = AppendTag(items, "X")

	// A correct AppendTag must not write "X" into the shared backing array, so
	// the element the caller can still observe at index 2 must remain "c".
	if backing[2] != "c" {
		t.Fatalf("AppendTag mutated the caller's backing array: backing[2] = %q, want %q",
			backing[2], "c")
	}
}
