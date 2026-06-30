package solution

import "context"

func Fetch(ctx context.Context, source func(context.Context) (int, error)) (int, error) {
	return source(ctx)
}
