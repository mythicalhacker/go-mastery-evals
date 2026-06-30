package solution

import "sync"

// BUG: every goroutine writes into one shared map with no synchronization.
// The Go runtime detects the concurrent writes and panics ("concurrent map
// writes"); even when it doesn't, racing read-modify-writes lose updates.
func CountConcurrent(values []int, workers int) map[int]int {
	if workers < 1 {
		workers = 1
	}
	n := len(values)
	result := make(map[int]int)
	var wg sync.WaitGroup
	for w := range workers {
		lo, hi := w*n/workers, (w+1)*n/workers
		wg.Add(1)
		go func() {
			defer wg.Done()
			for _, v := range values[lo:hi] {
				result[v]++
			}
		}()
	}
	wg.Wait()
	return result
}
