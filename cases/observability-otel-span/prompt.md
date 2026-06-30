Implement, in Go, package `solution` (no `main` function):

`DoWork(ctx context.Context) error` that performs a unit of work inside an OpenTelemetry trace span named `do-work`, sets an integer attribute `items` to `3` on the span, and returns `nil`. Obtain the tracer from the global tracer provider. Ensure the span is properly ended. Use `go.opentelemetry.io/otel`. Output only the Go code.
