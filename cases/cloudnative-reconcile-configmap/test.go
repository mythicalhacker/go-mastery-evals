package solution

import (
	"context"
	"maps"
	"testing"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

func TestReconcileCreatesThenIdempotent(t *testing.T) {
	c := fake.NewSimpleClientset()
	ctx := context.Background()
	want := map[string]string{"k": "v1"}
	if err := ReconcileConfigMap(ctx, c, "ns", "cfg", want); err != nil {
		t.Fatalf("first reconcile (create): %v", err)
	}
	if err := ReconcileConfigMap(ctx, c, "ns", "cfg", want); err != nil {
		t.Fatalf("second reconcile must be idempotent: %v", err)
	}
	cm, err := c.CoreV1().ConfigMaps("ns").Get(ctx, "cfg", metav1.GetOptions{})
	if err != nil {
		t.Fatalf("get: %v", err)
	}
	if !maps.Equal(cm.Data, want) {
		t.Fatalf("data = %v, want %v", cm.Data, want)
	}
}

func TestReconcileFixesDrift(t *testing.T) {
	c := fake.NewSimpleClientset()
	ctx := context.Background()
	_ = ReconcileConfigMap(ctx, c, "ns", "cfg", map[string]string{"k": "old"})
	want := map[string]string{"k": "new", "k2": "x"}
	if err := ReconcileConfigMap(ctx, c, "ns", "cfg", want); err != nil {
		t.Fatalf("reconcile drift: %v", err)
	}
	cm, _ := c.CoreV1().ConfigMaps("ns").Get(ctx, "cfg", metav1.GetOptions{})
	if !maps.Equal(cm.Data, want) {
		t.Fatalf("drift not fixed: data = %v", cm.Data)
	}
}
