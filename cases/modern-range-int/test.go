package solution

import (
	"slices"
	"testing"
)

func TestFirstN(t *testing.T) {
	if got := FirstN(3); !slices.Equal(got, []int{0, 1, 2}) {
		t.Fatalf("FirstN(3) = %v, want [0 1 2]", got)
	}
	if got := FirstN(0); len(got) != 0 {
		t.Fatalf("FirstN(0) = %v, want empty", got)
	}
	if got := FirstN(-2); len(got) != 0 {
		t.Fatalf("FirstN(-2) = %v, want empty", got)
	}
}
