package solution

import (
	"context"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
)

// BUG: never ends the span, so it is never exported/recorded (a span is only
// delivered to processors on End). The attribute is set but the span leaks.
func DoWork(ctx context.Context) error {
	_, span := otel.Tracer("solution").Start(ctx, "do-work")
	span.SetAttributes(attribute.Int("items", 3))
	_ = span
	return nil
}
