package solution

import (
	"strings"
	"testing"
	"time"
)

// Value-based assertions: tolerate incidental key casing, pin the behavior.
// The zero-time contract is the discriminator (omitzero omits it; omitempty
// does not, since a struct value is never "empty").

func TestMarshalOmitsZeroTime(t *testing.T) {
	b, err := Marshal(Event{Name: "alice"})
	if err != nil {
		t.Fatal(err)
	}
	s := string(b)
	if strings.Contains(s, "0001-01-01") {
		t.Fatalf("zero time must be omitted, but the zero value leaked: %s", s)
	}
	if strings.Contains(s, "when") {
		t.Fatalf("zero time must be omitted, but the \"when\" key is present: %s", s)
	}
}

func TestMarshalKeepsSetTime(t *testing.T) {
	when := time.Date(2024, 3, 1, 12, 0, 0, 0, time.UTC)
	b, err := Marshal(Event{Name: "bob", When: when})
	if err != nil {
		t.Fatal(err)
	}
	if s := string(b); !strings.Contains(s, "2024-03-01T12:00:00Z") {
		t.Fatalf("a set time must be present as RFC3339, got %s", s)
	}
}
