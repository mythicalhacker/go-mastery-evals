Implement, in Go, package `solution` (no `main` function):

A function `ReadInRoot(dir, name string) ([]byte, error)` that reads the file `name` and returns its contents, but only when `name` resolves to a location inside `dir`. The function must confine all access to `dir`: a `name` that tries to traverse outside it (for example `../secret` or another path that would escape the directory) must return an error instead of reading the file outside `dir`.

Use only the Go standard library. Output only the Go code.
