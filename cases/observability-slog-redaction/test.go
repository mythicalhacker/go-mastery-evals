package solution

import (
	"bytes"
	"log/slog"
	"strings"
	"testing"
)

func TestTokenRedacted(t *testing.T) {
	var buf bytes.Buffer
	l := slog.New(slog.NewTextHandler(&buf, nil))
	l.Info("auth", "cred", Credential{User: "alice", Token: "SECRET-XYZ"})
	out := buf.String()
	if strings.Contains(out, "SECRET-XYZ") {
		t.Fatalf("token leaked into log output: %s", out)
	}
	if !strings.Contains(out, "alice") {
		t.Fatalf("user missing from log output: %s", out)
	}
}
