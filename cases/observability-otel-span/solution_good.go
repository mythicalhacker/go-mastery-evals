package solution

import (
	"context"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
)

func DoWork(ctx context.Context) error {
	_, span := otel.Tracer("solution").Start(ctx, "do-work")
	defer span.End()
	span.SetAttributes(attribute.Int("items", 3))
	return nil
}
