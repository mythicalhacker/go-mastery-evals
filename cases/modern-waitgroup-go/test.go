package solution

import (
	"sync/atomic"
	"testing"
)

func TestProcessAll(t *testing.T) {
	var n atomic.Int64
	ProcessAll([]int{1, 2, 3, 4, 5}, func(int) { n.Add(1) })
	if n.Load() != 5 {
		t.Fatalf("processed %d items, want 5", n.Load())
	}
}
