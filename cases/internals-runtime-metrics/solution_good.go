package solution

import "runtime/metrics"

func HeapObjectsBytes() uint64 {
	const key = "/memory/classes/heap/objects:bytes"
	s := []metrics.Sample{{Name: key}}
	metrics.Read(s)
	return s[0].Value.Uint64()
}
