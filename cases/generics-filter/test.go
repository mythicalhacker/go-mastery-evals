package solution

import (
	"reflect"
	"testing"
)

func TestFilterInts(t *testing.T) {
	got := Filter([]int{1, 2, 3, 4}, func(n int) bool { return n%2 == 0 })
	want := []int{2, 4}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("Filter(ints) = %v, want %v", got, want)
	}
}

func TestFilterStrings(t *testing.T) {
	got := Filter([]string{"a", "bb", "ccc"}, func(s string) bool { return len(s) > 1 })
	want := []string{"bb", "ccc"}
	if !reflect.DeepEqual(got, want) {
		t.Fatalf("Filter(strings) = %v, want %v", got, want)
	}
}
