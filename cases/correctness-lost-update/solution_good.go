package solution

import (
	"sync"
	"sync/atomic"
)

func SumCounter(workers, increments int) int64 {
	var counter atomic.Int64
	var wg sync.WaitGroup
	for range workers {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for range increments {
				counter.Add(1)
			}
		}()
	}
	wg.Wait()
	return counter.Load()
}
