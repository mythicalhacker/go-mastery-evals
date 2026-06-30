package solution

import "sync"

func ProcessAll(items []int, f func(int)) {
	var wg sync.WaitGroup
	for _, item := range items {
		wg.Go(func() {
			f(item)
		})
	}
	wg.Wait()
}
