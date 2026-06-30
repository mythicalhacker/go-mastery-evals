package solution

import "sync"

// BUG: behaviorally correct but uses the pre-1.25 manual Add/Done bookkeeping
// instead of the WaitGroup.Go idiom the case asks for.
func ProcessAll(items []int, f func(int)) {
	var wg sync.WaitGroup
	for _, item := range items {
		wg.Add(1)
		go func() {
			defer wg.Done()
			f(item)
		}()
	}
	wg.Wait()
}
