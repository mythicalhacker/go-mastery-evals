package solution

import (
	"context"
	"errors"
	"testing"
	"time"
)

func TestFetchReturnsValue(t *testing.T) {
	v, err := Fetch(context.Background(), func(context.Context) (int, error) {
		return 7, nil
	})
	if err != nil || v != 7 {
		t.Fatalf("Fetch = (%d, %v), want (7, nil)", v, err)
	}
}

func TestFetchPropagatesDeadline(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()
	// Downstream blocks until ITS context is done, or 5s elapses.
	source := func(c context.Context) (int, error) {
		select {
		case <-c.Done():
			return 0, c.Err()
		case <-time.After(5 * time.Second):
			return 99, nil
		}
	}
	type res struct {
		v   int
		err error
	}
	done := make(chan res, 1)
	go func() {
		v, err := Fetch(ctx, source)
		done <- res{v, err}
	}()
	select {
	case r := <-done:
		if !errors.Is(r.err, context.DeadlineExceeded) {
			t.Fatalf("downstream did not observe the deadline: v=%d err=%v", r.v, r.err)
		}
	case <-time.After(2 * time.Second):
		t.Fatal("Fetch blocked past the 50ms deadline (ctx not propagated downstream)")
	}
}
