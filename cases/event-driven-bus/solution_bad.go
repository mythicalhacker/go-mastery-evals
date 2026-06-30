package solution

import "sync"

// BUG: subscribers get UNBUFFERED channels and Publish does a BLOCKING send
// (ch <- msg) while holding the lock. If a subscriber is not actively reading at
// the instant of Publish, the send blocks, which stalls the publisher and wedges
// the bus (the held lock blocks every other Subscribe/Publish too). Correct code
// uses buffered channels and a non-blocking send so the publisher never blocks.
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
	ch := make(chan string) // BUG: unbuffered
	b.mu.Lock()
	defer b.mu.Unlock()
	b.subs[topic] = append(b.subs[topic], ch)
	return ch
}

// Publish delivers msg to all current subscribers of topic.
func (b *Bus) Publish(topic, msg string) {
	b.mu.Lock()
	defer b.mu.Unlock()
	for _, ch := range b.subs[topic] {
		ch <- msg // BUG: blocking send under the lock; stalls if no reader is ready
	}
}

// Close shuts the bus down.
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
}
