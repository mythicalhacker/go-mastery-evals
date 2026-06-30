package solution

// Loader is meant to coalesce concurrent lookups for the same key so that
// the underlying fetch runs at most once per in-flight key.
type Loader struct{}

// Load returns the value for key. This implementation simply calls fetch
// every time without any deduplication of concurrent identical-key calls.
func (l *Loader) Load(key string, fetch func() (int, error)) (int, error) {
	v, err := fetch()
	if err != nil {
		return 0, err
	}
	return v, nil
}
