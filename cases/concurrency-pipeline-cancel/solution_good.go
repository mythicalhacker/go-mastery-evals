package solution

import "context"

func Squares(ctx context.Context, nums []int) <-chan int {
	stage1 := make(chan int)
	go func() {
		defer close(stage1)
		for _, n := range nums {
			select {
			case stage1 <- n:
			case <-ctx.Done():
				return
			}
		}
	}()

	out := make(chan int)
	go func() {
		defer close(out)
		for n := range stage1 {
			select {
			case out <- n * n:
			case <-ctx.Done():
				return
			}
		}
	}()
	return out
}
