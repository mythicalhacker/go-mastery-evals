package solution

import "fmt"

// BUG: raw string interpolation performs no HTML escaping, so a crafted name
// injects markup/script (XSS).
func RenderGreeting(name string) (string, error) {
	return fmt.Sprintf("<p>Hello, %s!</p>", name), nil
}
