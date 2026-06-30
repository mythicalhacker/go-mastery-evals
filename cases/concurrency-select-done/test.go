package solution

import (
	"context"
	"testing"
	"time"
)

func TestMergeReturnsValue(t *testing.T) {
	a := make(chan int, 1)
	a <- 5
	b := make(chan int)
	if v, ok := Merge(context.Background(), a, b); !ok || v != 5 {
		t.Fatalf("Merge = (%d, %v), want (5, true)", v, ok)
	}
}

func TestMergeHonorsCancel(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	a, b := make(chan int), make(chan int) // never delivered
	type res struct {
		v  int
		ok bool
	}
	done := make(chan res, 1)
	go func() {
		v, ok := Merge(ctx, a, b)
		done <- res{v, ok}
	}()
	cancel()
	select {
	case r := <-done:
		if r.ok || r.v != 0 {
			t.Fatalf("Merge = (%d, %v), want (0, false) on cancel", r.v, r.ok)
		}
	case <-time.After(1 * time.Second):
		t.Fatal("Merge blocked after cancel (select is missing a ctx.Done arm)")
	}
}
