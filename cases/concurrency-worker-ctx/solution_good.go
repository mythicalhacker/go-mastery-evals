package solution

import "context"

// Leak-free worker: selects on both jobs and ctx.Done() for *receive and send*,
// and always closes out on exit, so it never leaks or blocks after cancel.
func Run(ctx context.Context, jobs <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for {
			select {
			case j, ok := <-jobs:
				if !ok {
					return
				}
				select {
				case out <- j * 2:
				case <-ctx.Done():
					return
				}
			case <-ctx.Done():
				return
			}
		}
	}()
	return out
}
