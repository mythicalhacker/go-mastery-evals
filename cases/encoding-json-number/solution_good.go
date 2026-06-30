package solution

import "encoding/json"

// Decoding into an int64 struct field preserves the integer exactly; the JSON
// number is never routed through a float64, so values above 2^53 stay precise.
func ParseID(data []byte) (int64, error) {
	var v struct {
		ID int64 `json:"id"`
	}
	if err := json.Unmarshal(data, &v); err != nil {
		return 0, err
	}
	return v.ID, nil
}
