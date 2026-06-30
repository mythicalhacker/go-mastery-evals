package solution

import (
	"hash/crc32"
	"sort"
	"strconv"
)

// replicas is the number of virtual nodes placed on the ring per physical node.
// A high replica count spreads each node across the keyspace so that load is
// even and removing one node only affects the keys in that node's arcs.
const replicas = 100

// Ring is a consistent-hash ring. Each physical node is hashed onto many points
// (virtual nodes) on a circular keyspace; a key is owned by the first node point
// found clockwise from the key's hash.
type Ring struct {
	points []uint32          // sorted ring positions of all virtual nodes
	owner  map[uint32]string // ring position -> physical node
	nodes  map[string]bool   // set of physical nodes currently on the ring
}

// NewRing builds a ring containing the given nodes.
func NewRing(nodes ...string) *Ring {
	r := &Ring{
		owner: make(map[uint32]string),
		nodes: make(map[string]bool),
	}
	for _, n := range nodes {
		r.Add(n)
	}
	return r
}

func hash(s string) uint32 {
	return crc32.ChecksumIEEE([]byte(s))
}

// Add inserts a node and its virtual nodes into the ring.
func (r *Ring) Add(node string) {
	if r.nodes[node] {
		return
	}
	r.nodes[node] = true
	for i := 0; i < replicas; i++ {
		p := hash(node + "#" + strconv.Itoa(i))
		if _, exists := r.owner[p]; !exists {
			r.owner[p] = node
			r.points = append(r.points, p)
		}
	}
	sort.Slice(r.points, func(a, b int) bool { return r.points[a] < r.points[b] })
}

// Remove deletes a node and all of its virtual nodes from the ring.
func (r *Ring) Remove(node string) {
	if !r.nodes[node] {
		return
	}
	delete(r.nodes, node)
	kept := r.points[:0]
	for _, p := range r.points {
		if r.owner[p] == node {
			delete(r.owner, p)
			continue
		}
		kept = append(kept, p)
	}
	r.points = kept
}

// Get returns the node that owns key: the first ring point clockwise from the
// key's hash, wrapping around to the start of the ring.
func (r *Ring) Get(key string) string {
	if len(r.points) == 0 {
		return ""
	}
	h := hash(key)
	i := sort.Search(len(r.points), func(i int) bool { return r.points[i] >= h })
	if i == len(r.points) {
		i = 0 // wrap around the ring
	}
	return r.owner[r.points[i]]
}
