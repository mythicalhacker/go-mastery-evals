package solution

import "iter"

func Count(n int) iter.Seq[int] {
	return func(yield func(int) bool) {
		for i := 0; i < n; i++ {
			if !yield(i) { // consumer broke out of the range loop; stop producing
				return
			}
		}
	}
}
