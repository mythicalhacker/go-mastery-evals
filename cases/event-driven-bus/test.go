package solution

import (
	"testing"
	"time"
)

// recvOrFail reads one value from ch, failing the test (rather than hanging) if
// nothing arrives within the timeout. This is what makes a blocking bad
// implementation FAIL deterministically instead of deadlocking forever.
func recvOrFail(t *testing.T, ch <-chan string, what string) string {
	t.Helper()
	select {
	case v := <-ch:
		return v
	case <-time.After(2 * time.Second):
		t.Fatalf("timed out waiting for %s", what)
		return ""
	}
}

func TestPublishReachesAllSubscribers(t *testing.T) {
	b := NewBus()
	defer b.Close()

	s1 := b.Subscribe("t")
	s2 := b.Subscribe("t")

	msgs := []string{"a", "b", "c"}
	// Buffer (cap 64) is far larger than 3, so the GOOD version never blocks here
	// even though no one is reading yet.
	for _, m := range msgs {
		b.Publish("t", m)
	}

	for i, want := range msgs {
		if got := recvOrFail(t, s1, "s1 message"); got != want {
			t.Fatalf("s1 msg %d = %q, want %q", i, got, want)
		}
		if got := recvOrFail(t, s2, "s2 message"); got != want {
			t.Fatalf("s2 msg %d = %q, want %q", i, got, want)
		}
	}
}

func TestPublishNoSubscribersDoesNotBlock(t *testing.T) {
	b := NewBus()
	defer b.Close()

	done := make(chan struct{})
	go func() {
		b.Publish("empty", "ignored") // must be a prompt no-op, never a panic
		close(done)
	}()

	select {
	case <-done:
	case <-time.After(2 * time.Second):
		t.Fatal("Publish to a topic with no subscribers did not return promptly")
	}
}
