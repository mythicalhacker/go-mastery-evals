package solution

func SearchAny(values []int, match func(int) bool) (int, bool) {
	type result struct {
		v  int
		ok bool
	}
	// Buffered to len(values): every goroutine can deliver its result without
	// blocking, so none is stranded even when we return after the first match.
	ch := make(chan result, len(values))
	for _, v := range values {
		go func() {
			ch <- result{v, match(v)}
		}()
	}
	for range values {
		if r := <-ch; r.ok {
			return r.v, true
		}
	}
	return 0, false
}
