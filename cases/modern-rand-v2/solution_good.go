package solution

import "math/rand/v2"

func RollDice() int {
	return rand.IntN(6) + 1
}
