package solution

import "testing"

func TestParseServeParsesArgs(t *testing.T) {
	host, port, err := ParseServe([]string{"-host", "example.com", "-port", "9090"})
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if host != "example.com" {
		t.Fatalf("host = %q, want %q", host, "example.com")
	}
	if port != 9090 {
		t.Fatalf("port = %d, want %d", port, 9090)
	}
}

func TestParseServeDefaults(t *testing.T) {
	host, port, err := ParseServe(nil)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if host != "localhost" {
		t.Fatalf("host = %q, want %q", host, "localhost")
	}
	if port != 8080 {
		t.Fatalf("port = %d, want %d", port, 8080)
	}
}
