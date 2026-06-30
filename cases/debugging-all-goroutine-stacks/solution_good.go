package solution

import "runtime"

func DumpAllStacks() string {
	buf := make([]byte, 1<<20)
	n := runtime.Stack(buf, true) // true = every goroutine
	return string(buf[:n])
}
