package solution

import "github.com/cilium/ebpf"

func NewCounters() (*ebpf.Map, error) {
	return ebpf.NewMap(&ebpf.MapSpec{
		Name:       "counters",
		Type:       ebpf.Hash,
		KeySize:    4,
		ValueSize:  8,
		MaxEntries: 1024,
	})
}
