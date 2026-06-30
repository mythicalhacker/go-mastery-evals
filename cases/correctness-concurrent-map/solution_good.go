package solution

import "sync"

func CountConcurrent(values []int, workers int) map[int]int {
	if workers < 1 {
		workers = 1
	}
	n := len(values)
	partials := make([]map[int]int, workers)
	var wg sync.WaitGroup
	for w := range workers {
		lo, hi := w*n/workers, (w+1)*n/workers
		wg.Add(1)
		go func() {
			defer wg.Done()
			local := make(map[int]int) // each goroutine owns its own map
			for _, v := range values[lo:hi] {
				local[v]++
			}
			partials[w] = local
		}()
	}
	wg.Wait()

	result := make(map[int]int)
	for _, p := range partials {
		for k, c := range p {
			result[k] += c
		}
	}
	return result
}
