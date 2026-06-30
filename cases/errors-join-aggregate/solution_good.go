package solution

import "errors"

var (
	ErrEmptyName   = errors.New("name is empty")
	ErrNegativeAge = errors.New("age is negative")
)

func Validate(name string, age int) error {
	var errs []error
	if name == "" {
		errs = append(errs, ErrEmptyName)
	}
	if age < 0 {
		errs = append(errs, ErrNegativeAge)
	}
	return errors.Join(errs...)
}
