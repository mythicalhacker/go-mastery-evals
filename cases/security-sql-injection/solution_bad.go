package solution

import (
	"context"
	"database/sql"
	"fmt"
)

// BUG: builds the query with string interpolation, so a crafted email value
// can inject SQL. No parameter placeholder is used.
func GetUserByEmail(ctx context.Context, db *sql.DB, email string) (string, error) {
	var name string
	q := fmt.Sprintf("SELECT name FROM users WHERE email = '%s'", email)
	if err := db.QueryRowContext(ctx, q).Scan(&name); err != nil {
		return "", err
	}
	return name, nil
}
