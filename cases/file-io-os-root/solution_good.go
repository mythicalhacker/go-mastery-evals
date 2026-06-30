package solution

import "os"

func ReadInRoot(dir, name string) ([]byte, error) {
	root, err := os.OpenRoot(dir) // confines all access to dir
	if err != nil {
		return nil, err
	}
	defer root.Close()
	// ReadFile rejects names that traverse outside the root (e.g. "../secret").
	return root.ReadFile(name)
}
