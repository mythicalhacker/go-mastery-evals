package solution

import (
	"context"
	"testing"
	"time"
)

type ctxKey string

func TestDetachKeepsValues(t *testing.T) {
	parent := context.WithValue(context.Background(), ctxKey("user"), "alice")
	d := Detach(parent)
	if got, _ := d.Value(ctxKey("user")).(string); got != "alice" {
		t.Fatalf("value lost after Detach: got %q, want %q", got, "alice")
	}
}

func TestDetachIgnoresCancel(t *testing.T) {
	parent, cancel := context.WithCancel(context.Background())
	d := Detach(parent)
	cancel()
	time.Sleep(10 * time.Millisecond)
	if err := d.Err(); err != nil {
		t.Fatalf("detached context was cancelled: %v", err)
	}
	select {
	case <-d.Done():
		t.Fatal("detached context Done() fired after parent cancel")
	default:
	}
}
