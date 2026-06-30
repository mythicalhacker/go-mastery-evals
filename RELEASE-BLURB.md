# go-mastery — launch copy

Drop-in copy for the README, the launch post, and social. Everything here is backed by
[RESULTS.md](RESULTS.md); every number is reproducible with a `make` target.

The framing to hold onto: we're not just releasing a skill, we're releasing **a skill and the
benchmark that measures it**. The benchmark is the part that lasts. Anyone — us, JetBrains, a
community author, a skill that doesn't exist yet — can run the same gate and let the number
settle the argument.

---

## README blurb (long form)

### go-mastery

Most "best practices" Go skills ask you to trust them. This one ships with the receipts.

**go-mastery** is a skill that makes a model write production-grade, idiomatic Go — correct
concurrency with real shutdown paths, wrapped errors, current Go 1.21–1.26 APIs, parameterized
queries, hardened HTTP servers. **go-mastery-evals** is the open harness that proves it: it runs
every task twice, once with the skill and once without, and grades the output with the **Go
toolchain itself** — `go build`, `go vet`, `go test`, `golangci-lint` — plus a hidden behavioral
test the model never sees. No LLM-as-judge, no vibes. A case compiles, passes its test, and uses
the modern idiom, or it doesn't.

The result, measured across **two vendors and six models**:

- **+20.0 / +16.7 / +14.1 pp** correctness on Anthropic Haiku / Sonnet / Opus.
- **+26.3 / +20.7 / +12.6 pp** on OpenAI GPT‑5.4‑nano / GPT‑5.4‑mini / GPT‑5.5 — same direction,
  same shape, **not Claude-specific**.
- **Zero regressions** anywhere — no model got worse on a single case in any run.
- On the weakest model the skill **fixes 12 of the 15** tasks it fails on its own. On the strongest,
  where pass/fail saturates, a deterministic quality score still shows the code is more idiomatic
  (**+0.32** on already-passing Opus cases).

And against the field: **ahead of JetBrains `go-modern-guidelines` on every tier (+6.7 / +5.2 /
+4.5 pp) and never behind on a single case**, and ahead of the leading community-authored Go skill
by **+6.3 pp** with idiom density roughly level. Out of its domain — generic algorithm puzzles it
wasn't built for — it does no harm, staying neutral within sampling noise.

The benchmark is the bigger release. It's toolchain-graded, hermetic (vendored, offline),
deterministic where it can be and honest about sampling noise where it can't, and every case
validates its own discrimination with a must-pass and a must-fail fixture. If you maintain a Go
skill and think you can beat these numbers, the harness stages any skill identically — **prove
it**: `make baseline`. The leaderboard is meant to be public.

→ Full methodology, per-tier tables, head-to-heads, and reproduction: **[RESULTS.md](RESULTS.md)**

---

## README blurb (short form)

**go-mastery** makes models write production-grade, idiomatic Go — and it's *measured*, not
asserted. An open, toolchain-graded A/B harness (54 Go cases, hidden behavioral tests, hermetic
grading) shows the skill lifts correctness **+12 to +26 pp on every model of both Anthropic and
OpenAI with zero regressions**, and beats every other Go skill we benchmarked — JetBrains
`go-modern-guidelines` (+6.7/+5.2/+4.5 pp, never behind) and the leading community skill (+6.3 pp).
The harness ships too: run your own skill through the same gate. → [RESULTS.md](RESULTS.md)

---

## One-liner

> A Go skill that's verified, not claimed: +12–26 pp correctness across Anthropic *and* OpenAI,
> zero regressions, ahead of every other Go skill measured — with the open, toolchain-graded
> benchmark in the box so anyone can check, or try to beat it.

---

## Social / announcement (≤280 chars)

> Most Go "best practices" skills ask for trust. We shipped the receipts.
>
> go-mastery: +12–26pp correctness across Claude *and* GPT‑5, 0 regressions, beats every other Go
> skill we tested. Graded by the Go toolchain, not a model.
>
> And the benchmark's open — beat it.

---

## Notes for whoever posts this

- **JetBrains is named on purpose** — it's a commercial vendor and the comparison is fair game.
- **The community skill is deliberately not named.** Respect for individual maintainers comes
  first; the work can speak for itself, and the harness lets anyone reproduce the comparison
  without us putting a person's name in a marketing line. Keep it that way.
- **Lead with the benchmark, not the brag.** "We measured it and you can too" ages better than
  "we won." The numbers are strong enough to carry themselves.
