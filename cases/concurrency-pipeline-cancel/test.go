package solution

import (
	"context"
	"runtime"
	"slices"
	"testing"
	"time"
)

func waitSettled(base int, d time.Duration) bool {
	deadline := time.Now().Add(d)
	for {
		runtime.GC()
		if runtime.NumGoroutine() <= base+3 {
			return true
		}
		if time.Now().After(deadline) {
			return runtime.NumGoroutine() <= base+3
		}
		time.Sleep(10 * time.Millisecond)
	}
}

func TestSquaresFullDrain(t *testing.T) {
	out := Squares(context.Background(), []int{1, 2, 3, 4, 5})
	var got []int
	for v := range out {
		got = append(got, v)
	}
	if want := []int{1, 4, 9, 16, 25}; !slices.Equal(got, want) {
		t.Fatalf("got %v, want %v", got, want)
	}
}

func TestSquaresCancelNoLeak(t *testing.T) {
	base := runtime.NumGoroutine()
	nums := make([]int, 10)
	for i := range nums {
		nums[i] = i + 1
	}
	// Start a pipeline, read one value, cancel, then STOP reading. A clean
	// pipeline tears its stages down; a leaky one strands them blocked on send.
	for range 30 {
		ctx, cancel := context.WithCancel(context.Background())
		out := Squares(ctx, nums)
		<-out
		cancel()
		_ = out // deliberately stop reading
	}
	if !waitSettled(base, 3*time.Second) {
		t.Fatalf("goroutines leaked after mid-stream cancel: base=%d, now=%d",
			base, runtime.NumGoroutine())
	}
}
