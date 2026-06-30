package solution

import (
	"testing"
	"time"
)

func TestSameInstantDifferentZones(t *testing.T) {
	utc := time.Date(2024, 3, 1, 12, 0, 0, 0, time.UTC)
	loc := time.FixedZone("X+2", 2*3600)
	other := utc.In(loc) // same instant, different location (14:00 in X+2)
	if !SameInstant(utc, other) {
		t.Fatalf("SameInstant must be true for the same instant in different zones")
	}
}

func TestSameInstantDifferent(t *testing.T) {
	a := time.Date(2024, 3, 1, 12, 0, 0, 0, time.UTC)
	b := time.Date(2024, 3, 1, 12, 0, 1, 0, time.UTC) // one second later
	if SameInstant(a, b) {
		t.Fatalf("SameInstant must be false for different instants")
	}
}
