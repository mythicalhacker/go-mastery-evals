package solution

import (
	"hash/crc32"
	"sort"
)

// BUG: maps keys with `nodes[hash(key) % len(nodes)]`. This is NOT consistent
// hashing: when a node is removed, len(nodes) changes and the modulo shifts the
// index for almost every key, reshuffling the whole keyspace across the
// remaining nodes instead of moving only the removed node's keys.
type Ring struct {
	nodes []string // kept sorted for determinism
}

func NewRing(nodes ...string) *Ring {
	r := &Ring{}
	for _, n := range nodes {
		r.Add(n)
	}
	return r
}

func (r *Ring) Add(node string) {
	for _, n := range r.nodes {
		if n == node {
			return
		}
	}
	r.nodes = append(r.nodes, node)
	sort.Strings(r.nodes)
}

func (r *Ring) Remove(node string) {
	for i, n := range r.nodes {
		if n == node {
			r.nodes = append(r.nodes[:i], r.nodes[i+1:]...)
			return
		}
	}
}

func (r *Ring) Get(key string) string {
	if len(r.nodes) == 0 {
		return ""
	}
	h := crc32.ChecksumIEEE([]byte(key))
	return r.nodes[h%uint32(len(r.nodes))]
}
