package solution

import "syscall/js"

// BUG: syscall/js only exists for GOOS=js, not wasip1 — this does not compile for WASI.
func Timestamp() int64 {
	return int64(js.Global().Get("Date").Call("now").Float()) / 1000
}
