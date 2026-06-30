package solution

import (
	"bytes"
	"html/template"
)

var greetTmpl = template.Must(template.New("greet").Parse(`<p>Hello, {{.}}!</p>`))

func RenderGreeting(name string) (string, error) {
	var b bytes.Buffer
	if err := greetTmpl.Execute(&b, name); err != nil {
		return "", err
	}
	return b.String(), nil
}
