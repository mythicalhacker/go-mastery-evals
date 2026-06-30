package solution

import (
	"context"
	"errors"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func RecoveryInterceptor(ctx context.Context, req any, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (resp any, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = status.Errorf(codes.Internal, "panic recovered: %v", r)
		}
	}()
	resp, err = handler(ctx, req)
	if err != nil {
		switch {
		case errors.Is(err, context.DeadlineExceeded):
			return nil, status.FromContextError(context.DeadlineExceeded).Err()
		case errors.Is(err, context.Canceled):
			return nil, status.FromContextError(context.Canceled).Err()
		}
	}
	return resp, err
}
