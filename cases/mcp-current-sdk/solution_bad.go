package solution

import "github.com/modelcontextprotocol/go-sdk/mcp"

// BUG: pre-1.0 API. NewServer took (name, version, opts); tools were added via
// s.AddTools(mcp.NewServerTool(...)). None of this exists in the v1.x SDK.
func BuildServer() *mcp.Server {
	s := mcp.NewServer("greeter", "1.0.0", nil)
	s.AddTools(mcp.NewServerTool("greet", "greet someone", nil))
	return s
}
