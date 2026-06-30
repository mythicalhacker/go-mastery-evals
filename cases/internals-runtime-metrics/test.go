package solution

import (
	"runtime"
	"testing"
)

func TestHeapObjectsBytesNonzero(t *testing.T) {
	// Allocate something live so the heap has objects, and keep it
	// reachable past the measurement so it isn't collected.
	buf := make([]byte, 1<<20)
	for i := range buf {
		buf[i] = byte(i)
	}

	got := HeapObjectsBytes()
	if got == 0 {
		t.Fatalf("HeapObjectsBytes() = 0, want > 0")
	}

	runtime.KeepAlive(buf)
}
