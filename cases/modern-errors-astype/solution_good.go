package solution

import "errors"

type NotFound struct{ Key string }

func (e *NotFound) Error() string { return "not found: " + e.Key }

func Lookup(err error) (string, bool) {
	if nf, ok := errors.AsType[*NotFound](err); ok {
		return nf.Key, true
	}
	return "", false
}
