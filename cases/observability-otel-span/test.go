package solution

import (
	"context"
	"testing"

	"go.opentelemetry.io/otel"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	"go.opentelemetry.io/otel/sdk/trace/tracetest"
)

func TestDoWorkRecordsEndedSpan(t *testing.T) {
	sr := tracetest.NewSpanRecorder()
	otel.SetTracerProvider(sdktrace.NewTracerProvider(sdktrace.WithSpanProcessor(sr)))

	if err := DoWork(context.Background()); err != nil {
		t.Fatalf("DoWork: %v", err)
	}
	spans := sr.Ended()
	if len(spans) != 1 {
		t.Fatalf("want exactly 1 ended span, got %d (did you call span.End()?)", len(spans))
	}
	if got := spans[0].Name(); got != "do-work" {
		t.Fatalf("span name = %q, want do-work", got)
	}
	ok := false
	for _, a := range spans[0].Attributes() {
		if string(a.Key) == "items" && a.Value.AsInt64() == 3 {
			ok = true
		}
	}
	if !ok {
		t.Fatalf("missing attribute items=3; got %v", spans[0].Attributes())
	}
}
