package solution

import (
	"errors"
	"fmt"
	"strings"
)

var (
	ErrEmptyName   = errors.New("name is empty")
	ErrNegativeAge = errors.New("age is negative")
)

// BUG: flattens causes into a single string, so errors.Is can no longer
// match either sentinel.
func Validate(name string, age int) error {
	var msgs []string
	if name == "" {
		msgs = append(msgs, ErrEmptyName.Error())
	}
	if age < 0 {
		msgs = append(msgs, ErrNegativeAge.Error())
	}
	if len(msgs) == 0 {
		return nil
	}
	return fmt.Errorf("validation failed: %s", strings.Join(msgs, "; "))
}
