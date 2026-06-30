package solution

import (
	"testing"
)

func equal(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func TestNSmallestAscending(t *testing.T) {
	got := NSmallest([]int{5, 2, 8, 1, 9, 3}, 3)
	want := []int{1, 2, 3}
	if !equal(got, want) {
		t.Fatalf("NSmallest([5 2 8 1 9 3], 3) = %v, want %v", got, want)
	}
}

func TestNSmallestDuplicates(t *testing.T) {
	got := NSmallest([]int{4, 4, 4}, 2)
	want := []int{4, 4}
	if !equal(got, want) {
		t.Fatalf("NSmallest([4 4 4], 2) = %v, want %v", got, want)
	}
}
