package solution

import (
	"fmt"
	"os"
)

func ReadConfig(path string) ([]byte, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read config %q: %w", path, err)
	}
	return b, nil
}
