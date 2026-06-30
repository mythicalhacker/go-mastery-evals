package solution

import "sync"

// subBuffer is the per-subscriber channel capacity. A generous buffer lets the
// non-blocking send in Publish succeed for reasonable bursts without dropping.
const subBuffer = 64

// Bus is a concurrency-safe in-process pub/sub bus.
type Bus struct {
	mu     sync.Mutex
	subs   map[string][]chan string
	closed bool
}

// NewBus returns a ready-to-use Bus.
func NewBus() *Bus {
	return &Bus{subs: make(map[string][]chan string)}
}

// Subscribe registers a new subscriber for topic and returns its channel.
func (b *Bus) Subscribe(topic string) <-chan string {
	ch := make(chan string, subBuffer) // buffered so Publish need not wait on a reader
	b.mu.Lock()
	defer b.mu.Unlock()
	if b.closed {
		close(ch) // bus is done; hand back an already-closed channel
		return ch
	}
	b.subs[topic] = append(b.subs[topic], ch)
	return ch
}

// Publish delivers msg to all current subscribers of topic. It never blocks the
// caller: each send is non-blocking, so a slow or full subscriber is skipped
// rather than stalling the publisher. A topic with no subscribers is a no-op.
func (b *Bus) Publish(topic, msg string) {
	b.mu.Lock()
	defer b.mu.Unlock()
	if b.closed {
		return
	}
	for _, ch := range b.subs[topic] {
		select {
		case ch <- msg:
		default: // subscriber's buffer is full; do not block the publisher
		}
	}
}

// Close shuts the bus down, closing every subscriber channel exactly once.
func (b *Bus) Close() {
	b.mu.Lock()
	defer b.mu.Unlock()
	if b.closed {
		return
	}
	b.closed = true
	for _, chans := range b.subs {
		for _, ch := range chans {
			close(ch)
		}
	}
	b.subs = make(map[string][]chan string)
}
