package solution

import "flag"

// BUG: uses package-level flags on the global flag set and calls flag.Parse(),
// which reads os.Args instead of the passed-in args. The `args` parameter is
// ignored entirely, so callers (and tests) that pass explicit args get the
// defaults back. This is also not isolated: it mutates global flag state.
var (
	hostFlag = flag.String("host", "localhost", "listen host")
	portFlag = flag.Int("port", 8080, "listen port")
)

func ParseServe(args []string) (host string, port int, err error) {
	flag.Parse() // reads os.Args, not args
	return *hostFlag, *portFlag, nil
}
