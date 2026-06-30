package solution

import "net/netip"

func InCIDR(cidr, ip string) (bool, error) {
	prefix, err := netip.ParsePrefix(cidr)
	if err != nil {
		return false, err
	}
	addr, err := netip.ParseAddr(ip)
	if err != nil {
		return false, err
	}
	// Masked() zeroes any host bits in the prefix so membership is correct
	// even when the CIDR is written with host bits set (e.g. 10.1.2.255/24).
	return prefix.Masked().Contains(addr), nil
}
