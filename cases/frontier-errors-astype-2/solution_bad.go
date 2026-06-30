package solution

import "errors"

type RateLimited struct {
	RetryAfterSeconds int
}

func (e RateLimited) Error() string {
	return "rate limited"
}

func RetryAfter(err error) (int, bool) {
	var e RateLimited
	if errors.As(err, &e) {
		return e.RetryAfterSeconds, true
	}
	return 0, false
}
