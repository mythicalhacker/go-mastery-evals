package solution

import "testing"

func TestNewSettingsValues(t *testing.T) {
	s := NewSettings(5, "prod")
	if s == nil {
		t.Fatal("NewSettings returned nil")
	}
	if s.Retries == nil {
		t.Fatal("Retries pointer is nil")
	}
	if s.Label == nil {
		t.Fatal("Label pointer is nil")
	}
	if *s.Retries != 5 {
		t.Errorf("*Retries = %d, want 5", *s.Retries)
	}
	if *s.Label != "prod" {
		t.Errorf("*Label = %q, want %q", *s.Label, "prod")
	}
}

func TestNewSettingsIndependentCopies(t *testing.T) {
	retries := 7
	label := "staging"

	s := NewSettings(retries, label)

	// Mutate the originals after the call. The struct must hold independent
	// copies, so the pointed-to values must not change.
	retries = 99
	label = "mutated"

	if *s.Retries != 7 {
		t.Errorf("*Retries = %d, want 7 (mutating original arg leaked into struct)", *s.Retries)
	}
	if *s.Label != "staging" {
		t.Errorf("*Label = %q, want %q (mutating original arg leaked into struct)", *s.Label, "staging")
	}
}

func TestNewSettingsDistinctPointers(t *testing.T) {
	a := NewSettings(1, "a")
	b := NewSettings(1, "a")

	if a.Retries == b.Retries {
		t.Error("Retries pointers from separate calls must be distinct")
	}
	if a.Label == b.Label {
		t.Error("Label pointers from separate calls must be distinct")
	}

	// Mutating one must not affect the other.
	*a.Retries = 1000
	if *b.Retries == 1000 {
		t.Error("mutating one Settings affected another")
	}
}
