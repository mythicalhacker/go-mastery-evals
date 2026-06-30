package solution

import (
	"encoding/json"
	"fmt"
)

// BUG: decoding into map[string]any makes encoding/json store the number as a
// float64, which cannot represent integers above 2^53 exactly. Converting that
// float64 to int64 silently rounds 9007199254740993 down to 9007199254740992.
func ParseID(data []byte) (int64, error) {
	var m map[string]any
	if err := json.Unmarshal(data, &m); err != nil {
		return 0, err
	}
	f, ok := m["id"].(float64)
	if !ok {
		return 0, fmt.Errorf("id field missing or not a number")
	}
	return int64(f), nil
}
