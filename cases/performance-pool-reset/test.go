package solution

import "testing"

func TestPooledBufferAlwaysClean(t *testing.T) {
	bp := NewBufferPool()
	for i := 0; i < 100; i++ {
		b := bp.Get()
		if b.Len() != 0 {
			t.Fatalf("Get returned a dirty buffer (len=%d) on iteration %d", b.Len(), i)
		}
		b.WriteString("stale-data")
		bp.Put(b)
	}
}
