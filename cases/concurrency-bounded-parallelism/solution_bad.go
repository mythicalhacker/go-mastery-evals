package solution

import "sync"

// BUG: ignores `limit` and fans out one goroutine per item, so all invocations
// of f run at once. Correct code caps in-flight work with a semaphore.
func MapConcurrent(items []int, limit int, f func(int) int) []int {
	out := make([]int, len(items))
	var wg sync.WaitGroup
	for i, v := range items {
		wg.Add(1)
		go func() {
			defer wg.Done()
			out[i] = f(v)
		}()
	}
	wg.Wait()
	return out
}
