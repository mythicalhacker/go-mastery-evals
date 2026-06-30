Implement, in Go, package `solution` (no `main` function):

A function `GetUserByEmail(ctx context.Context, db *sql.DB, email string) (string, error)` that returns the `name` column for the row in the `users` table whose `email` matches the argument. Use `database/sql`. The query must be safe against SQL injection.

Output only the Go code.
