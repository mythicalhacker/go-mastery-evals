package solution

import "net/http"

// BUG: no timeouts configured. A bare *http.Server uses unbounded read/write
// deadlines, leaving it open to slow-loris exhaustion.
func NewServer(addr string, h http.Handler) *http.Server {
	return &http.Server{
		Addr:    addr,
		Handler: h,
	}
}
