package solution

import "time"

func Timestamp() int64 {
	return time.Now().Unix()
}
