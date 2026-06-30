package solution

import "sync"

func MapConcurrent(items []int, limit int, f func(int) int) []int {
	out := make([]int, len(items))
	sem := make(chan struct{}, limit) // buffered channel as a counting semaphore
	var wg sync.WaitGroup
	for i, v := range items {
		sem <- struct{}{} // acquire a slot; blocks once `limit` are in flight
		wg.Add(1)
		go func() {
			defer wg.Done()
			defer func() { <-sem }() // release the slot
			out[i] = f(v)
		}()
	}
	wg.Wait()
	return out
}
