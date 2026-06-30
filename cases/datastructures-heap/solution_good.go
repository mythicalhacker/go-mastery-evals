package solution

import "container/heap"

// intHeap is a min-heap of ints implementing heap.Interface.
type intHeap []int

func (h intHeap) Len() int           { return len(h) }
func (h intHeap) Less(i, j int) bool { return h[i] < h[j] } // min-heap: smallest at the root
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
		out = append(out, heap.Pop(&h).(int)) // each Pop yields the current minimum
	}
	return out
}
