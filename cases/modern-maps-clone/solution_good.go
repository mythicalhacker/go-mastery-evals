package solution

import "maps"

func Copy(m map[string]int) map[string]int {
	return maps.Clone(m)
}
