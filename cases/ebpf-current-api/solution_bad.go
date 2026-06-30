package solution

import "github.com/cilium/ebpf"

// BUG: MapSpec.RewriteConstants was removed from cilium/ebpf; code emitted from
// older training data still calls it and no longer compiles against current versions.
func NewCounters() (*ebpf.Map, error) {
	spec := &ebpf.MapSpec{Name: "counters", Type: ebpf.Hash, KeySize: 4, ValueSize: 8, MaxEntries: 1024}
	spec.RewriteConstants(map[string]interface{}{"x": uint32(1)})
	return ebpf.NewMap(spec)
}
