package solution

import "context"

// BUG: the stages ignore ctx on their sends. If the consumer stops reading after
// cancelling, each stage blocks forever on its send and never returns, so the
// stage goroutines (and their channels) leak.
func Squares(ctx context.Context, nums []int) <-chan int {
	stage1 := make(chan int)
	go func() {
		defer close(stage1)
		for _, n := range nums {
			stage1 <- n
		}
	}()

	out := make(chan int)
	go func() {
		defer close(out)
		for n := range stage1 {
			out <- n * n
		}
	}()
	return out
}
