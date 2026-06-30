Implement, in Go, package `solution` (no `main` function):

A function `ParseServe(args []string) (host string, port int, err error)` that parses the flags for a `serve` subcommand out of its own argument slice `args` (for example `[]string{"-host", "example.com", "-port", "9090"}`).

It must support two flags: `-host` (a string, default `"localhost"`) and `-port` (an int, default `8080`). On success it returns the parsed values and a nil error; if `args` cannot be parsed it returns the parse error.

The function must be self-contained and testable: it must parse the values out of `args` itself and must not rely on the global `flag` package state or on `os.Args`.

Use only the Go standard library. Output only the Go code.
