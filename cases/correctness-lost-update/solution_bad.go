package solution

import "sync"

// BUG: counter++ is an unsynchronized read-modify-write shared across goroutines.
// Under contention the racing updates clobber one another, so the final total
// comes out well below workers*increments.
func SumCounter(workers, increments int) int64 {
	var counter int64
	var wg sync.WaitGroup
	for range workers {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for range increments {
				counter++
			}
		}()
	}
	wg.Wait()
	return counter
}
