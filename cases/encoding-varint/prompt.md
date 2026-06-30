Implement two functions in Go (package `solution`) for the **standard library / protobuf variable-length integer encoding** (LEB128, little-endian base-128):

```go
// EncodeUvarints encodes each value as an unsigned varint and concatenates the
// results, using Go's standard library variable-length encoding.
func EncodeUvarints(nums []uint64) []byte

// DecodeUvarints decodes a buffer produced by EncodeUvarints back into the
// original sequence. It returns an error if the buffer is malformed/truncated.
func DecodeUvarints(data []byte) ([]uint64, error)
```

Requirements:
- Use the encoding where the **least-significant** 7-bit group comes first and the high bit (`0x80`) marks "more bytes follow" — i.e. `128` encodes to `0x80 0x01`. This is what `encoding/binary`'s varint functions and the protobuf wire format use.
- `DecodeUvarints` must consume the buffer sequentially and error on a truncated final varint.

Output exactly one Go code block and nothing else.
