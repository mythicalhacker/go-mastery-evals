package solution

import "testing"

func TestRollDice(t *testing.T) {
	seen := map[int]bool{}
	for range 1000 {
		v := RollDice()
		if v < 1 || v > 6 {
			t.Fatalf("RollDice() = %d, want within [1,6]", v)
		}
		seen[v] = true
	}
	if len(seen) < 2 {
		t.Fatalf("RollDice produced only %d distinct value(s) over 1000 calls", len(seen))
	}
}
