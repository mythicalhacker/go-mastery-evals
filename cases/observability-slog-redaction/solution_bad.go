package solution

// BUG: no slog.LogValuer implementation, so slog renders every field of the
// struct, leaking Token into the logs.
type Credential struct {
	User  string
	Token string
}
