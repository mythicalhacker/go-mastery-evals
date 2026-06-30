Implement, in Go, package `solution` (no `main` function):

A function `InCIDR(cidr, ip string) (bool, error)` that reports whether the address `ip` falls inside the network described by `cidr`. For example, `InCIDR("10.0.0.0/8", "10.1.2.3")` returns `true`, while `InCIDR("10.0.0.0/8", "11.0.0.1")` returns `false`.

Return a non-nil error if `cidr` or `ip` cannot be parsed.

Use only the Go standard library. Output only the Go code.
