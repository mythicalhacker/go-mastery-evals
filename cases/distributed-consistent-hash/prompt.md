Implement, in Go, package `solution` (no `main` function):

A consistent-hash ring that maps string keys to nodes.

Provide:

- `NewRing(nodes ...string) *Ring` — construct a ring containing the given nodes.
- `(*Ring) Add(node string)` — add a node to the ring.
- `(*Ring) Remove(node string)` — remove a node from the ring.
- `(*Ring) Get(key string) string` — return the node that owns `key`.

Requirement: use consistent hashing so that removal causes only minimal disruption. When a node is removed, every key that was NOT mapped to the removed node must continue to map to the SAME node it did before — only the removed node's keys may move. Do not reshuffle keys across the remaining nodes when the membership changes.

Use only the Go standard library. Output only the Go code.
