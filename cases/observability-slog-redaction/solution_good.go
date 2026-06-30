package solution

import "log/slog"

type Credential struct {
	User  string
	Token string
}

// LogValue controls how slog renders a Credential: Token is deliberately omitted.
func (c Credential) LogValue() slog.Value {
	return slog.GroupValue(slog.String("user", c.User))
}
