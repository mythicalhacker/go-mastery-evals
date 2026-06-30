package solution

import "runtime/debug"

// BUG: debug.Stack() captures only the calling goroutine's stack, which is
// useless for finding a deadlock or leak in another goroutine.
func DumpAllStacks() string {
	return string(debug.Stack())
}
