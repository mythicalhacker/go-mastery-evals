Implement, in Go, package `solution` (no `main` function):

A gRPC unary **server** interceptor `RecoveryInterceptor` of type `grpc.UnaryServerInterceptor` that hardens an RPC handler:

1. If the handler panics, recover and return the error as a gRPC **status** error with code `Internal` (the panic must not crash the server).
2. If the handler returns an error that is (or wraps) `context.DeadlineExceeded` or `context.Canceled`, return it as a gRPC status error carrying the corresponding gRPC code (`DeadlineExceeded` / `Canceled`).
3. Otherwise return the handler's response and error unchanged.

Use `google.golang.org/grpc` and its `codes`/`status` packages. Output only the Go code.
