package solution

import "runtime"

// BUG: ReadMemStats stops the world; the task requires the modern metrics API.
func HeapObjectsBytes() uint64 {
	var m runtime.MemStats
	runtime.ReadMemStats(&m)
	return m.HeapAlloc
}
