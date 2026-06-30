package solution

import (
	"encoding/json"
	"time"
)

// BUG: the empty-omitting tag option does not drop a zero time.Time (a struct
// value is never considered "empty"), so the zero When is still emitted. The
// 1.24 zero-omitting option is required here.
type Event struct {
	Name string    `json:"name"`
	When time.Time `json:"when,omitempty"`
}

func Marshal(e Event) ([]byte, error) {
	return json.Marshal(e)
}
