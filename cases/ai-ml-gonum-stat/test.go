package solution

import (
	"math"
	"testing"
)

func TestMeanStd(t *testing.T) {
	xs := []float64{2, 4, 4, 4, 5, 5, 7, 9}

	mean, std := MeanStd(xs)

	if math.Abs(mean-5) > 1e-9 {
		t.Fatalf("mean: want 5, got %v", mean)
	}

	// gonum's sample standard deviation for xs is ~2.138.
	// The bad solution returns the variance (~4.571) and fails this band.
	if std < 2.10 || std > 2.18 {
		t.Fatalf("std: want sample stddev in [2.10, 2.18], got %v", std)
	}
}
