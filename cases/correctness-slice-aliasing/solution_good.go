package solution

import "slices"

func AppendTag(items []string, tag string) []string {
	return append(slices.Clone(items), tag)
}
