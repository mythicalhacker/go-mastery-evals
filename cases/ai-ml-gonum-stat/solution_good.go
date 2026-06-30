package solution

import "gonum.org/v1/gonum/stat"

func MeanStd(xs []float64) (mean, std float64) {
	return stat.Mean(xs, nil), stat.StdDev(xs, nil)
}
