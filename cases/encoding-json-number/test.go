package solution

import "testing"

func TestParseIDLargeExact(t *testing.T) {
	// 9007199254740993 == 2^53 + 1, the smallest integer a float64 cannot hold.
	const want int64 = 9007199254740993
	got, err := ParseID([]byte(`{"id":9007199254740993}`))
	if err != nil {
		t.Fatalf("ParseID returned error: %v", err)
	}
	if got != want {
		t.Fatalf("ParseID = %d, want %d (precision lost)", got, want)
	}
}

func TestParseIDSmall(t *testing.T) {
	const want int64 = 42
	got, err := ParseID([]byte(`{"id":42}`))
	if err != nil {
		t.Fatalf("ParseID returned error: %v", err)
	}
	if got != want {
		t.Fatalf("ParseID = %d, want %d", got, want)
	}
}
