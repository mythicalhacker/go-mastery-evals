package solution

import (
	"testing"
)

// collectFirst3 ranges over Count(10) and breaks after 3 values. With a correct
// iterator this returns cleanly; with an iterator that ignores yield's result,
// the runtime panics when the loop breaks. The panic propagates out of this
// helper and fails the test.
func collectFirst3() []int {
	var got []int
	for v := range Count(10) {
		got = append(got, v)
		if len(got) == 3 {
			break
		}
	}
	return got
}

func TestCountEarlyBreak(t *testing.T) {
	got := collectFirst3() // panics here for an iterator that ignores yield's bool
	want := []int{0, 1, 2}
	if len(got) != len(want) {
		t.Fatalf("Count(10) first-3 = %v, want %v", got, want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("Count(10) first-3 = %v, want %v", got, want)
		}
	}
}

func TestCountFullRange(t *testing.T) {
	var got []int
	for v := range Count(5) {
		got = append(got, v)
	}
	want := []int{0, 1, 2, 3, 4}
	if len(got) != len(want) {
		t.Fatalf("Count(5) = %v, want %v", got, want)
	}
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("Count(5) = %v, want %v", got, want)
		}
	}
}
