package solution

import "time"

func SameInstant(a, b time.Time) bool {
	return a.Equal(b)
}
