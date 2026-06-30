package solution

import (
	"os"
	"path/filepath"
)

// BUG: filepath.Join cleans the path, collapsing ".." segments, so a name like
// "../secret.txt" escapes dir and is read anyway. Nothing confines access to
// dir. Correct code anchors the read to the directory and rejects escapes.
func ReadInRoot(dir, name string) ([]byte, error) {
	return os.ReadFile(filepath.Join(dir, name))
}
