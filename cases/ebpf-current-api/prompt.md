Implement, in Go, package `solution` (no `main` function):

`NewCounters() (*ebpf.Map, error)` that creates an eBPF **hash** map named `counters` with 4-byte keys, 8-byte values, and 1024 max entries, using `github.com/cilium/ebpf`. Use only APIs present in current releases of the library. Output only the Go code.
