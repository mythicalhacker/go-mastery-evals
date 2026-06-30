package solution

import (
	"context"
	"database/sql"
)

func GetUserByEmail(ctx context.Context, db *sql.DB, email string) (string, error) {
	var name string
	err := db.QueryRowContext(ctx,
		"SELECT name FROM users WHERE email = $1", email).Scan(&name)
	if err != nil {
		return "", err
	}
	return name, nil
}
