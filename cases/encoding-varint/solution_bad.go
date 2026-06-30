package solution

import "errors"

// BAD: emits MSB-first (MIDI/Git-style) VLQ instead of LEB128/protobuf LSB-first.
// 128 becomes 0x81 0x00 instead of the required 0x80 0x01 — byte-reversed, and it
// agrees with the correct encoding only for values < 128, so trivial cases pass.
func EncodeUvarints(nums []uint64) []byte {
	var buf []byte
	for _, n := range nums {
		b := []byte{byte(n & 0x7f)}
		for n >>= 7; n > 0; n >>= 7 {
			b = append([]byte{byte(n&0x7f | 0x80)}, b...)
		}
		buf = append(buf, b...)
	}
	return buf
}

func DecodeUvarints(data []byte) ([]uint64, error) {
	return nil, errors.New("not implemented")
}
