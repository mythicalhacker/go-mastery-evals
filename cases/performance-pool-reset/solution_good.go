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

func (bp *BufferPool) Put(b *bytes.Buffer) {
	b.Reset()
	bp.p.Put(b)
}
