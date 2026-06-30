package solution

import "testing"

func TestSumCounter(t *testing.T) {
	// High contention: 64 goroutines each doing 50k unsynchronized increments
	// lose updates on essentially every run, so the total comes out short.
	const workers, increments = 64, 50000
	got := SumCounter(workers, increments)
	want := int64(workers * increments)
	if got != want {
		t.Fatalf("SumCounter = %d, want %d (lost updates: counter not synchronized)", got, want)
	}
}

func TestSumCounterSmall(t *testing.T) {
	if got := SumCounter(1, 1000); got != 1000 {
		t.Fatalf("SumCounter(1, 1000) = %d, want 1000", got)
	}
}
