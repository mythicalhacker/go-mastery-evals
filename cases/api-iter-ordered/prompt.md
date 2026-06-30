Implement, in Go, package `solution` (no `main` function):

A type `Counter` that tallies occurrences of string keys.

1. A method `Add(key string)` that increments the count for `key`.
2. An iteration method `All()` that lets a caller range over the recorded
   (key, count) pairs like this:

   ```go
   for k, n := range c.All() {
       // k is a key, n is its count
   }
   ```

   The pairs must be visited in ascending key order, and this order must be
   the same on every iteration. Do not expose the internal map (callers must
   not be able to mutate it through the value returned by `All()`).

Use only the Go standard library. Output only the Go code.
