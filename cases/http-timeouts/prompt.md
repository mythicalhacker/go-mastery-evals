Implement, in Go, package `solution` (no `main` function):

A function `NewServer(addr string, h http.Handler) *http.Server` that returns a production-ready `*http.Server` bound to `addr` using handler `h`, configured with sensible timeouts that protect against slow-client (slow-loris) attacks.

Output only the Go code.
