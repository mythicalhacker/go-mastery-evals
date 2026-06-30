package solution

import (
	"context"
	"testing"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func invoke(h grpc.UnaryHandler) (any, error) {
	return RecoveryInterceptor(context.Background(), "req", &grpc.UnaryServerInfo{FullMethod: "/svc/M"}, h)
}

func TestPanicBecomesInternal(t *testing.T) {
	_, err := invoke(func(ctx context.Context, req any) (any, error) { panic("boom") })
	if status.Code(err) != codes.Internal {
		t.Fatalf("panic: want codes.Internal, got %v (%v)", status.Code(err), err)
	}
}

func TestDeadlineCode(t *testing.T) {
	_, err := invoke(func(ctx context.Context, req any) (any, error) { return nil, context.DeadlineExceeded })
	if status.Code(err) != codes.DeadlineExceeded {
		t.Fatalf("deadline: want codes.DeadlineExceeded, got %v", status.Code(err))
	}
}

func TestCanceledCode(t *testing.T) {
	_, err := invoke(func(ctx context.Context, req any) (any, error) { return nil, context.Canceled })
	if status.Code(err) != codes.Canceled {
		t.Fatalf("canceled: want codes.Canceled, got %v", status.Code(err))
	}
}

func TestSuccessPassthrough(t *testing.T) {
	resp, err := invoke(func(ctx context.Context, req any) (any, error) { return "out", nil })
	if err != nil || resp != "out" {
		t.Fatalf("ok path: want (out,nil), got (%v,%v)", resp, err)
	}
}
