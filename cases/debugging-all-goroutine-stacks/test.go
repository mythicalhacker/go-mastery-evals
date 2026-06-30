package solution

import (
	"strings"
	"sync"
	"testing"
	"time"
)

func parkedWorker(release <-chan struct{}) { <-release }

func TestDumpIncludesOtherGoroutines(t *testing.T) {
	var wg sync.WaitGroup
	release := make(chan struct{})
	const n = 5
	for i := 0; i < n; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			parkedWorker(release)
		}()
	}
	time.Sleep(50 * time.Millisecond) // let them block

	dump := DumpAllStacks()

	close(release)
	wg.Wait()

	if c := strings.Count(dump, "goroutine "); c < 3 {
		t.Fatalf("expected many goroutines in dump, found %d", c)
	}
	if !strings.Contains(dump, "parkedWorker") {
		t.Fatalf("dump does not include the parked worker goroutines")
	}
}
