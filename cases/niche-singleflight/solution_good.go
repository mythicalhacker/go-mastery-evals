package solution

import "golang.org/x/sync/singleflight"

// Loader coalesces concurrent lookups for the same key so that the
// underlying fetch runs at most once per in-flight key.
type Loader struct {
	group singleflight.Group
}

// Load returns the value for key. When several goroutines call Load with
// the same key at the same time, fetch executes only once and every
// caller receives that shared result. Distinct keys proceed independently.
func (l *Loader) Load(key string, fetch func() (int, error)) (int, error) {
	v, err, _ := l.group.Do(key, func() (any, error) {
		return fetch()
	})
	if err != nil {
		return 0, err
	}
	return v.(int), nil
}
