package solution

import "context"

// BUG: a fresh Background context drops every request-scoped value.
func Detach(ctx context.Context) context.Context {
	return context.Background()
}
