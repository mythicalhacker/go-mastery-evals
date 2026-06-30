package solution

import "errors"

type RateLimited struct {
	RetryAfterSeconds int
}

func (e RateLimited) Error() string {
	return "rate limited"
}

func RetryAfter(err error) (int, bool) {
	if e, ok := errors.AsType[RateLimited](err); ok {
		return e.RetryAfterSeconds, true
	}
	return 0, false
}
