Implement, in Go, package `solution` (no `main` function):

A type `Tags []string` that can be stored in and loaded from a single SQL text column. It must implement the standard `database/sql` interfaces so that the database layer can serialize the slice to one string by joining the elements with commas, and parse that string back into the slice. Provide both directions:

- Serializing: a `Tags` value turns into a comma-joined string (e.g. `Tags{"a", "b", "c"}` becomes `"a,b,c"`).
- Loading: a value read from the column turns back into the equivalent `Tags`. The loaded value may arrive as either a `string` or a `[]byte`, and a database `NULL` must produce an empty `Tags`.

Output only the Go code.
