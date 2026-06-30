Implement, in Go, package `solution` (no `main` function):

`ReconcileConfigMap(ctx context.Context, client kubernetes.Interface, namespace, name string, desired map[string]string) error`

It must make the ConfigMap named `name` in `namespace` match `desired`:
- if the ConfigMap does not exist, create it with `Data = desired`;
- if it exists but its `Data` differs, update it to `desired`;
- if it already matches, do nothing.

It must be **idempotent** (safe to call repeatedly) and handle the not-found case correctly using the API machinery error helpers. Use `k8s.io/client-go`. Output only the Go code.
