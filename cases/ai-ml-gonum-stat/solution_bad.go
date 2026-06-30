package solution

import "gonum.org/v1/gonum/stat"

// BUG: returns the variance, not the standard deviation (missing sqrt).
func MeanStd(xs []float64) (mean, std float64) {
	return stat.Mean(xs, nil), stat.Variance(xs, nil)
}
