package solution

import "context"

// BUG: ignores cancellation entirely. When jobs is neither written nor
// closed, the range blocks forever and the worker never closes out after the
// context is cancelled — a goroutine leak. Fails TestRunStopsOnCancel.
func Run(ctx context.Context, jobs <-chan int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for j := range jobs {
			out <- j * 2
		}
	}()
	return out
}
