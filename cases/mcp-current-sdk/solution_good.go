package solution

import (
	"context"

	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type greetIn struct {
	Name string `json:"name"`
}
type greetOut struct {
	Message string `json:"message"`
}

func greet(ctx context.Context, req *mcp.CallToolRequest, in greetIn) (*mcp.CallToolResult, greetOut, error) {
	return nil, greetOut{Message: "hi " + in.Name}, nil
}

func BuildServer() *mcp.Server {
	s := mcp.NewServer(&mcp.Implementation{Name: "greeter", Version: "1.0.0"}, nil)
	mcp.AddTool(s, &mcp.Tool{Name: "greet", Description: "greet someone"}, greet)
	return s
}
