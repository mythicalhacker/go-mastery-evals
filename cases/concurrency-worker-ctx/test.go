package solution

import (
	"context"
	"testing"
	"time"
)

func TestRunDoublesThenCloses(t *testing.T) {
	jobs := make(chan int)
	out := Run(context.Background(), jobs)
	go func() {
		for i := 1; i <= 3; i++ {
			jobs <- i
		}
		close(jobs)
	}()
	var got []int
	for v := range out { // terminates only if Run closes out
		got = append(got, v)
	}
	if len(got) != 3 || got[0] != 2 || got[2] != 6 {
		t.Fatalf("got %v, want [2 4 6]", got)
	}
}

func TestRunStopsOnCancel(t *testing.T) {
	jobs := make(chan int)
	ctx, cancel := context.WithCancel(context.Background())
	out := Run(ctx, jobs)
	cancel()
	select {
	case <-out: // closed channel returns immediately; a value is fine too
	case <-time.After(2 * time.Second):
		t.Fatal("Run did not stop after context cancellation (goroutine leak)")
	}
}
