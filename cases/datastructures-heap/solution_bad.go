package solution

import "container/heap"

// BUG: Less uses `>`, making this a max-heap. It still satisfies heap.Interface
// and compiles, but heap.Pop now returns the LARGEST element each time, so
// NSmallest returns the k largest in descending order instead of the k smallest
// in ascending order.
type intHeap []int

func (h intHeap) Len() int           { return len(h) }
func (h intHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h intHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *intHeap) Push(x any) {
	*h = append(*h, x.(int))
}

func (h *intHeap) Pop() any {
	old := *h
	n := len(old)
	v := old[n-1]
	*h = old[:n-1]
	return v
}

func NSmallest(nums []int, k int) []int {
	h := make(intHeap, len(nums))
	copy(h, nums)
	heap.Init(&h)

	out := make([]int, 0, k)
	for i := 0; i < k; i++ {
		out = append(out, heap.Pop(&h).(int))
	}
	return out
}
