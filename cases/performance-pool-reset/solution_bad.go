package solution

import (
	"bytes"
	"sync"
)

type BufferPool struct {
	p sync.Pool
}

func NewBufferPool() *BufferPool {
	return &BufferPool{p: sync.Pool{New: func() any { return new(bytes.Buffer) }}}
}

func (bp *BufferPool) Get() *bytes.Buffer {
	return bp.p.Get().(*bytes.Buffer)
}

// BUG: returns the buffer to the pool without resetting it, so the next Get
// observes stale bytes from the previous user.
func (bp *BufferPool) Put(b *bytes.Buffer) {
	bp.p.Put(b)
}
