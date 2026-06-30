package solution

import (
	"bytes"
	"testing"
)

func TestEncodeKnownVectors(t *testing.T) {
	// LEB128 / protobuf: least-significant 7-bit group first, 0x80 = continuation.
	cases := []struct {
		n    uint64
		want []byte
	}{
		{0, []byte{0x00}},
		{1, []byte{0x01}},
		{127, []byte{0x7f}},
		{128, []byte{0x80, 0x01}},
		{300, []byte{0xac, 0x02}},
		{16384, []byte{0x80, 0x80, 0x01}},
	}
	for _, c := range cases {
		got := EncodeUvarints([]uint64{c.n})
		if !bytes.Equal(got, c.want) {
			t.Fatalf("EncodeUvarints(%d) = % x, want % x (LEB128 is little-endian / LSB-first)", c.n, got, c.want)
		}
	}
}

func TestRoundTrip(t *testing.T) {
	in := []uint64{0, 1, 127, 128, 300, 16384, 1<<32 + 7, 1<<63 + 1}
	out, err := DecodeUvarints(EncodeUvarints(in))
	if err != nil {
		t.Fatalf("DecodeUvarints: %v", err)
	}
	if len(out) != len(in) {
		t.Fatalf("decoded %d values, want %d", len(out), len(in))
	}
	for i := range in {
		if out[i] != in[i] {
			t.Fatalf("round-trip[%d] = %d, want %d", i, out[i], in[i])
		}
	}
}

func TestDecodeTruncatedErrors(t *testing.T) {
	// A lone 0x80 promises a continuation byte that never arrives.
	if _, err := DecodeUvarints([]byte{0x80}); err == nil {
		t.Fatal("DecodeUvarints([0x80]) = nil error, want error on truncated input")
	}
}
