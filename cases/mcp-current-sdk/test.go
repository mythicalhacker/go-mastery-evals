package solution

import "testing"

func TestBuildServerNotNil(t *testing.T) {
	if BuildServer() == nil {
		t.Fatal("BuildServer() returned nil")
	}
}
