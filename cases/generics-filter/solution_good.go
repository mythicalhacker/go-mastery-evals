package solution

func Filter[T any](s []T, keep func(T) bool) []T {
	out := make([]T, 0)
	for _, v := range s {
		if keep(v) {
			out = append(out, v)
		}
	}
	return out
}
