package solution

import (
	"math/rand"
	"time"
)

// BUG: legacy global generator with manual seeding instead of the modern
// auto-seeded API. The seeding call has been deprecated since Go 1.20.
func RollDice() int {
	rand.Seed(time.Now().UnixNano())
	return rand.Intn(6) + 1
}
