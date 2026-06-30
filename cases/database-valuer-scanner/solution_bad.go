package solution

import (
	"database/sql/driver"
	"fmt"
	"strings"
)

type Tags []string

// Value serializes the slice to a single comma-joined string.
func (t Tags) Value() (driver.Value, error) {
	return strings.Join(t, ","), nil
}

// BUG: Scan only handles string. Database drivers commonly hand text columns
// back as []byte, which falls through to the error path, so loading a value
// that was just stored fails to round-trip.
func (t *Tags) Scan(src any) error {
	s, ok := src.(string)
	if !ok {
		return fmt.Errorf("Tags.Scan: unsupported source type %T", src)
	}
	*t = strings.Split(s, ",")
	return nil
}
