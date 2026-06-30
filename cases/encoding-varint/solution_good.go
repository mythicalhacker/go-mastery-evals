package solution

import (
	"encoding/binary"
	"errors"
)

// EncodeUvarints encodes each value as an unsigned varint (LEB128, the stdlib /
// protobuf wire format) and concatenates the results.
func EncodeUvarints(nums []uint64) []byte {
	buf := make([]byte, 0, len(nums)*2)
	var tmp [binary.MaxVarintLen64]byte
	for _, n := range nums {
		k := binary.PutUvarint(tmp[:], n)
		buf = append(buf, tmp[:k]...)
	}
	return buf
}

// DecodeUvarints reverses EncodeUvarints, erroring on a truncated final varint.
func DecodeUvarints(data []byte) ([]uint64, error) {
	out := make([]uint64, 0)
	for len(data) > 0 {
		v, k := binary.Uvarint(data)
		if k <= 0 {
			return nil, errors.New("decode uvarints: malformed or truncated input")
		}
		out = append(out, v)
		data = data[k:]
	}
	return out, nil
}
