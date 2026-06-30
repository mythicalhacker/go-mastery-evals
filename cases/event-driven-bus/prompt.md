Implement, in Go, package `solution` (no `main` function):

An in-process publish/subscribe `Bus`. Provide a constructor and these methods:

- `NewBus() *Bus` — returns a new, ready-to-use bus.
- `Subscribe(topic string) <-chan string` — registers a new subscriber for `topic` and returns a channel on which that subscriber receives messages.
- `Publish(topic, msg string)` — delivers `msg` to all current subscribers of `topic`.
- `Close()` — shuts the bus down.

Requirements:

- `Publish` delivers a message to all current subscribers of that topic.
- `Publish` must NOT block the caller, and must NOT panic when a topic has no subscribers.
- Concurrent `Subscribe` and `Publish` calls must be safe.

Use only the Go standard library. Output only the Go code.
