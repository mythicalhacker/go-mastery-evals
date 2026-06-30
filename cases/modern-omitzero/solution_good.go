package solution

import (
	"encoding/json"
	"time"
)

type Event struct {
	Name string    `json:"name"`
	When time.Time `json:"when,omitzero"`
}

func Marshal(e Event) ([]byte, error) {
	return json.Marshal(e)
}
