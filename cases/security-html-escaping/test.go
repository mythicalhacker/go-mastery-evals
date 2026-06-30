package solution

import (
	"strings"
	"testing"
)

func TestEscapesScript(t *testing.T) {
	out, err := RenderGreeting("<script>alert(1)</script>")
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(out, "<script>") {
		t.Fatalf("unescaped script tag in output: %q", out)
	}
	if !strings.Contains(out, "&lt;script&gt;") {
		t.Fatalf("expected HTML-escaped output, got: %q", out)
	}
}

func TestNormalNamePreserved(t *testing.T) {
	out, err := RenderGreeting("Alice")
	if err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(out, "Hello, Alice!") {
		t.Fatalf("greeting missing for normal name: %q", out)
	}
}
