package solution

// Settings holds optional configuration values as pointers so that the
// absence of a value can be distinguished from a zero value.
type Settings struct {
	Retries *int
	Label   *string
}

// NewSettings builds a *Settings whose fields point to independent copies
// of the provided arguments.
func NewSettings(retries int, label string) *Settings {
	return &Settings{
		Retries: new(retries),
		Label:   new(label),
	}
}
