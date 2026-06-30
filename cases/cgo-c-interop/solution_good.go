package solution

/*
static int square(int n) { return n * n; }
*/
import "C"

func Square(n int) int {
	return int(C.square(C.int(n)))
}
