package solution

import "context"

// BUG: passes a fresh background context downstream, discarding the caller's
// deadline/cancellation, so `source` never observes it and can run unbounded.
func Fetch(ctx context.Context, source func(context.Context) (int, error)) (int, error) {
	return source(context.Background())
}
