Implement, in Go, package `solution` (no `main` function):

A type `Credential` with exported fields `User string` and `Token string`. It must integrate with `log/slog` so that whenever a `Credential` is logged, the `Token` value never appears in the output — only `User` should be logged.

Output only the Go code.
