package solution

/*
static int square(int n) { return n * n; }
*/
import "C"

// BUG: a Go int cannot be passed where C.int is expected; must convert with C.int(n).
func Square(n int) int {
	return int(C.square(n))
}
