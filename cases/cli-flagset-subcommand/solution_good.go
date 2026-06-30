package solution

import "flag"

func ParseServe(args []string) (host string, port int, err error) {
	fs := flag.NewFlagSet("serve", flag.ContinueOnError) // isolated, not the global flag set
	hostFlag := fs.String("host", "localhost", "listen host")
	portFlag := fs.Int("port", 8080, "listen port")
	if err := fs.Parse(args); err != nil { // parses the passed args, not os.Args
		return "", 0, err
	}
	return *hostFlag, *portFlag, nil
}
