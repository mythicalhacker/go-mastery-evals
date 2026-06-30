package solution

import "context"

func Merge(ctx context.Context, a, b <-chan int) (int, bool) {
	select {
	case v := <-a:
		return v, true
	case v := <-b:
		return v, true
	case <-ctx.Done():
		return 0, false
	}
}
