package solution

import (
	"context"
	"fmt"

	"google.golang.org/grpc"
)

// BUG 1: recovers but returns a plain error (gRPC code Unknown, not Internal).
// BUG 2: passes context errors straight through, so they never become the proper
// DeadlineExceeded/Canceled status codes.
func RecoveryInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (resp any, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf("panic recovered: %v", r)
		}
	}()
	return handler(ctx, req)
}
