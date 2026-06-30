package solution

import (
	"net/netip"
	"strings"
)

// BUG: parses inputs correctly but decides membership with a textual prefix
// check on the network address string. Address text is not aligned to CIDR
// boundaries, so this misjudges hosts whose text does not literally start
// with the network base (e.g. 10.1.2.55 vs base "10.1.2.0", or any host in
// 10.0.0.0/8 other than 10.0.x.y). Correct code compares the masked network.
func InCIDR(cidr, ip string) (bool, error) {
	prefix, err := netip.ParsePrefix(cidr)
	if err != nil {
		return false, err
	}
	addr, err := netip.ParseAddr(ip)
	if err != nil {
		return false, err
	}
	base := prefix.Addr().String() // network address text, e.g. "10.1.2.0"
	return strings.HasPrefix(addr.String(), base), nil
}
