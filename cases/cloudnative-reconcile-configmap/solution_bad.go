package solution

import (
	"context"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

// BUG: always Creates — not idempotent (returns AlreadyExists on the 2nd call)
// and never reconciles drifted Data.
func ReconcileConfigMap(ctx context.Context, client kubernetes.Interface, namespace, name string, desired map[string]string) error {
	_, err := client.CoreV1().ConfigMaps(namespace).Create(ctx, &corev1.ConfigMap{
		ObjectMeta: metav1.ObjectMeta{Name: name, Namespace: namespace},
		Data:       desired,
	}, metav1.CreateOptions{})
	return err
}
