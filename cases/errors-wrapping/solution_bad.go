package solution

import (
	"fmt"
	"os"
)

// BUG: formats the cause with the value verb instead of the wrap verb,
// flattening it to a string. The wrapped fs.ErrNotExist is lost, so callers
// can no longer match it with errors.Is.
func ReadConfig(path string) ([]byte, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read config %q: %v", path, err)
	}
	return b, nil
}
