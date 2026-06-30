//go:build tools

// Pins the heavier (non-stdlib, non-x) dependencies that niche behavioral cases
// build against, so `go mod vendor` captures them. Build-tag-gated ("tools") so
// it never participates in a candidate build/vet/test.
package solution

import (
	_ "google.golang.org/grpc"
	_ "google.golang.org/grpc/codes"
	_ "google.golang.org/grpc/credentials/insecure"
	_ "google.golang.org/grpc/metadata"
	_ "google.golang.org/grpc/status"
	_ "google.golang.org/grpc/test/bufconn"
	_ "google.golang.org/protobuf/proto"

	_ "k8s.io/api/core/v1"
	_ "k8s.io/apimachinery/pkg/api/errors"
	_ "k8s.io/apimachinery/pkg/apis/meta/v1"
	_ "k8s.io/client-go/kubernetes"
	_ "k8s.io/client-go/kubernetes/fake"
	_ "go.opentelemetry.io/otel"
	_ "go.opentelemetry.io/otel/attribute"
	_ "go.opentelemetry.io/otel/sdk/trace"
	_ "go.opentelemetry.io/otel/sdk/trace/tracetest"
	_ "go.opentelemetry.io/otel/trace"

	_ "github.com/cilium/ebpf"
	_ "github.com/modelcontextprotocol/go-sdk/mcp"

	_ "gonum.org/v1/gonum/mat"
	_ "gonum.org/v1/gonum/stat"
)
