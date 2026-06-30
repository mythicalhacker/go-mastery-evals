package solution

import (
	"context"
	"maps"

	corev1 "k8s.io/api/core/v1"
	apierrors "k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

func ReconcileConfigMap(ctx context.Context, client kubernetes.Interface, namespace, name string, desired map[string]string) error {
	cms := client.CoreV1().ConfigMaps(namespace)
	existing, err := cms.Get(ctx, name, metav1.GetOptions{})
	if apierrors.IsNotFound(err) {
		_, err = cms.Create(ctx, &corev1.ConfigMap{
			ObjectMeta: metav1.ObjectMeta{Name: name, Namespace: namespace},
			Data:       desired,
		}, metav1.CreateOptions{})
		return err
	}
	if err != nil {
		return err
	}
	if maps.Equal(existing.Data, desired) {
		return nil
	}
	existing.Data = desired
	_, err = cms.Update(ctx, existing, metav1.UpdateOptions{})
	return err
}
