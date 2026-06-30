package solution

import (
	"errors"
	"testing"
)

func TestBothFailuresMatchable(t *testing.T) {
	err := Validate("", -1)
	if err == nil {
		t.Fatal("expected an error")
	}
	if !errors.Is(err, ErrEmptyName) {
		t.Error("error does not match ErrEmptyName")
	}
	if !errors.Is(err, ErrNegativeAge) {
		t.Error("error does not match ErrNegativeAge")
	}
}

func TestSingleFailure(t *testing.T) {
	err := Validate("ok", -1)
	if !errors.Is(err, ErrNegativeAge) {
		t.Fatalf("want ErrNegativeAge, got %v", err)
	}
	if errors.Is(err, ErrEmptyName) {
		t.Error("unexpected ErrEmptyName match")
	}
}

func TestNoFailureIsNil(t *testing.T) {
	if err := Validate("ok", 1); err != nil {
		t.Fatalf("want nil, got %v", err)
	}
}
