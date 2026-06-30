package solution

import (
	"reflect"
	"testing"
)

func TestTagsRoundTrip(t *testing.T) {
	v, err := Tags{"a", "b", "c"}.Value()
	if err != nil {
		t.Fatalf("Value returned error: %v", err)
	}

	var got Tags
	if err := got.Scan(v); err != nil {
		t.Fatalf("Scan(Value()) returned error: %v", err)
	}
	if want := (Tags{"a", "b", "c"}); !reflect.DeepEqual(got, want) {
		t.Fatalf("round trip = %#v, want %#v", got, want)
	}
}

func TestTagsScanBytes(t *testing.T) {
	var got Tags
	if err := got.Scan([]byte("x,y")); err != nil {
		t.Fatalf("Scan([]byte) returned error: %v", err)
	}
	if want := (Tags{"x", "y"}); !reflect.DeepEqual(got, want) {
		t.Fatalf("Scan([]byte) = %#v, want %#v", got, want)
	}
}

func TestTagsScanNil(t *testing.T) {
	var got Tags
	if err := got.Scan(nil); err != nil {
		t.Fatalf("Scan(nil) returned error: %v", err)
	}
	if len(got) != 0 {
		t.Fatalf("Scan(nil) = %#v, want empty", got)
	}
}
