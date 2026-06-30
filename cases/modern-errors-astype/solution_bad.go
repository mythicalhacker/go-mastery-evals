package solution

import "errors"

type NotFound struct{ Key string }

func (e *NotFound) Error() string { return "not found: " + e.Key }

// BUG: functionally correct but uses the pre-1.26 errors.As idiom instead of
// the typed errors.AsType the case asks for.
func Lookup(err error) (string, bool) {
	var nf *NotFound
	if errors.As(err, &nf) {
		return nf.Key, true
	}
	return "", false
}
