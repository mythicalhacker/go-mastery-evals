package solution

import "testing"

func TestSquare(t *testing.T) {
	if got := Square(5); got != 25 {
		t.Fatalf("Square(5) = %d, want 25", got)
	}
	if got := Square(-3); got != 9 {
		t.Fatalf("Square(-3) = %d, want 9", got)
	}
}
