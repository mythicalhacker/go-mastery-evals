package solution

import "strconv"

// BUG: ignores the unit suffix entirely, so "2KB", "1MB", "100B" all parse
// wrong (and "" / "abc" don't error as required). Fails the behavioral test.
func ParseSize(s string) (int64, error) {
	n, err := strconv.ParseInt(s, 10, 64)
	return n, err
}
