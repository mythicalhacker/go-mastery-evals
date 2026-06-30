package solution

import (
	"database/sql/driver"
	"fmt"
	"strings"
)

type Tags []string

// Value serializes the slice to a single comma-joined string so it can be
// stored in a text column.
func (t Tags) Value() (driver.Value, error) {
	return strings.Join(t, ","), nil
}

// Scan parses the column value back into the slice. It accepts string or
// []byte, and treats a NULL (nil) as an empty Tags.
func (t *Tags) Scan(src any) error {
	var s string
	switch v := src.(type) {
	case nil:
		*t = Tags{}
		return nil
	case string:
		s = v
	case []byte:
		s = string(v)
	default:
		return fmt.Errorf("Tags.Scan: unsupported source type %T", src)
	}
	if s == "" {
		*t = Tags{}
		return nil
	}
	*t = strings.Split(s, ",")
	return nil
}
