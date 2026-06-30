package solution

import "context"

// BUG: the select has no ctx.Done() arm. When neither channel ever delivers and
// the context is cancelled, it blocks forever instead of returning (0, false).
func Merge(ctx context.Context, a, b <-chan int) (int, bool) {
	select {
	case v := <-a:
		return v, true
	case v := <-b:
		return v, true
	}
}
