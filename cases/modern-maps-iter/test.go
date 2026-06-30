package solution

import (
	"slices"
	"testing"
)

func TestSortedKeys(t *testing.T) {
	m := map[string]int{"b": 2, "a": 1, "c": 3}
	if got := SortedKeys(m); !slices.Equal(got, []string{"a", "b", "c"}) {
		t.Fatalf("SortedKeys = %v, want [a b c]", got)
	}
	if got := SortedKeys(map[string]int{}); len(got) != 0 {
		t.Fatalf("SortedKeys(empty) = %v, want empty", got)
	}
}
