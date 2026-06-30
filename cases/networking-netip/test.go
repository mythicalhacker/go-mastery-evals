package solution

import "testing"

func TestInCIDRMembership(t *testing.T) {
	cases := []struct {
		cidr, ip string
		want     bool
	}{
		{"10.0.0.0/8", "10.1.2.3", true},
		{"192.168.0.0/16", "192.168.5.9", true},
		{"10.0.0.0/8", "11.0.0.1", false},
		// A naive string-prefix check on the network base ("10.1.2.0") would
		// report false here because "10.1.2.55" does not start with that text.
		{"10.1.2.0/24", "10.1.2.55", true},
		// Just outside the /24.
		{"10.1.2.0/24", "10.1.3.1", false},
	}
	for _, c := range cases {
		got, err := InCIDR(c.cidr, c.ip)
		if err != nil {
			t.Fatalf("InCIDR(%q, %q) returned unexpected error: %v", c.cidr, c.ip, err)
		}
		if got != c.want {
			t.Fatalf("InCIDR(%q, %q) = %v, want %v", c.cidr, c.ip, got, c.want)
		}
	}
}

func TestInCIDRMalformed(t *testing.T) {
	if _, err := InCIDR("not-a-cidr", "10.0.0.1"); err == nil {
		t.Fatalf("InCIDR with malformed cidr: expected an error, got nil")
	}
	if _, err := InCIDR("10.0.0.0/8", "not-an-ip"); err == nil {
		t.Fatalf("InCIDR with malformed ip: expected an error, got nil")
	}
}
