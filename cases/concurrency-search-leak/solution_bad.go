package solution

import "sync"

// BUG: results go to an UNBUFFERED channel and only matching goroutines send.
// After the first match we return; the other matching goroutines are then stuck
// forever on `ch <- v` (no receiver) -> goroutine leak. The done channel guards
// only the no-match case, not the leak.
func SearchAny(values []int, match func(int) bool) (int, bool) {
	ch := make(chan int)
	done := make(chan struct{})
	var wg sync.WaitGroup
	for _, v := range values {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if match(v) {
				ch <- v
			}
		}()
	}
	go func() {
		wg.Wait()
		close(done)
	}()
	select {
	case v := <-ch:
		return v, true
	case <-done:
		return 0, false
	}
}
