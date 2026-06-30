package solution

import (
	"errors"
	"io/fs"
	"testing"
)

func TestReadConfigWrapsNotExist(t *testing.T) {
	_, err := ReadConfig("/no/such/file/definitely-missing-xyz-123")
	if err == nil {
		t.Fatal("expected an error for a missing file")
	}
	if !errors.Is(err, fs.ErrNotExist) {
		t.Fatalf("returned error does not wrap fs.ErrNotExist: %v", err)
	}
}
