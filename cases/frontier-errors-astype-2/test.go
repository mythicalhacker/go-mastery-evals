package solution

import (
	"errors"
	"fmt"
	"testing"
)

func TestRetryAfterDoublyWrapped(t *testing.T) {
	wrapped := fmt.Errorf("outer: %w", fmt.Errorf("mid: %w", RateLimited{RetryAfterSeconds: 30}))
	secs, ok := RetryAfter(wrapped)
	if !ok || secs != 30 {
		t.Fatalf("RetryAfter(wrapped) = (%d, %v), want (30, true)", secs, ok)
	}
}

func TestRetryAfterDirect(t *testing.T) {
	secs, ok := RetryAfter(RateLimited{RetryAfterSeconds: 5})
	if !ok || secs != 5 {
		t.Fatalf("RetryAfter(direct) = (%d, %v), want (5, true)", secs, ok)
	}
}

func TestRetryAfterAbsent(t *testing.T) {
	secs, ok := RetryAfter(errors.New("nope"))
	if ok || secs != 0 {
		t.Fatalf("RetryAfter(unrelated) = (%d, %v), want (0, false)", secs, ok)
	}
}

func TestRetryAfterNil(t *testing.T) {
	secs, ok := RetryAfter(nil)
	if ok || secs != 0 {
		t.Fatalf("RetryAfter(nil) = (%d, %v), want (0, false)", secs, ok)
	}
}
