package solution

import (
	"bytes"
	"os"
	"path/filepath"
	"testing"
)

func TestReadInRootReadsFileInside(t *testing.T) {
	base := t.TempDir()
	dir := filepath.Join(base, "dir")
	if err := os.Mkdir(dir, 0o755); err != nil {
		t.Fatalf("mkdir: %v", err)
	}
	if err := os.WriteFile(filepath.Join(dir, "data.txt"), []byte("ok"), 0o644); err != nil {
		t.Fatalf("write data.txt: %v", err)
	}

	got, err := ReadInRoot(dir, "data.txt")
	if err != nil {
		t.Fatalf("ReadInRoot(dir, \"data.txt\") returned error: %v", err)
	}
	if !bytes.Equal(got, []byte("ok")) {
		t.Fatalf("ReadInRoot(dir, \"data.txt\") = %q, want %q", got, "ok")
	}
}

func TestReadInRootRejectsTraversal(t *testing.T) {
	base := t.TempDir()
	dir := filepath.Join(base, "dir")
	if err := os.Mkdir(dir, 0o755); err != nil {
		t.Fatalf("mkdir: %v", err)
	}
	// secret.txt is a sibling of dir, OUTSIDE the confined directory.
	if err := os.WriteFile(filepath.Join(base, "secret.txt"), []byte("SECRET"), 0o644); err != nil {
		t.Fatalf("write secret.txt: %v", err)
	}

	got, err := ReadInRoot(dir, "../secret.txt")
	if err == nil {
		t.Fatalf("ReadInRoot(dir, \"../secret.txt\") returned nil error; traversal must be rejected (got %q)", got)
	}
	if bytes.Equal(got, []byte("SECRET")) {
		t.Fatalf("ReadInRoot(dir, \"../secret.txt\") leaked contents outside dir: %q", got)
	}
}
