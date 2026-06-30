//go:build tools

// Package solution's tools file pins the allowed golang.org/x/* dependencies so
// `go mod vendor` captures them. It is build-tag-gated ("tools"), so it is
// excluded from every candidate build/vet/test — it exists only to drive
// vendoring. To allow another x/* package, add a blank import here and re-run
// `make vendor`. Arbitrary third-party imports remain unvendored, so a
// candidate that reaches for them fails to build (by design).
package solution

import (
	_ "golang.org/x/exp/constraints"
	_ "golang.org/x/sync/errgroup"
	_ "golang.org/x/sync/semaphore"
	_ "golang.org/x/sync/singleflight"
	_ "golang.org/x/time/rate"
)
