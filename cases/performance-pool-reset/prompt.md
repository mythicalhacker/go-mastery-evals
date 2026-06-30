Implement, in Go, package `solution` (no `main` function):

A `BufferPool` that recycles `*bytes.Buffer` values via `sync.Pool`, with:
- `func NewBufferPool() *BufferPool`
- `func (p *BufferPool) Get() *bytes.Buffer`
- `func (p *BufferPool) Put(b *bytes.Buffer)`

A buffer handed out by `Get` must always be empty and ready to use, even after a previous user wrote to it and returned it via `Put`.

Output only the Go code.
