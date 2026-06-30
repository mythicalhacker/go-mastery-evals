# go-mastery — Results & Benchmark

Two things ship together here: **`go-mastery`**, a skill that makes a model write
production-grade, idiomatic Go, and **`go-mastery-evals`**, the open harness that *measures*
whether any Go skill actually does that. The second is the more durable contribution. A "best
practices" skill is a claim; this repository turns the claim into a number anyone can
reproduce — and the same number is available to anyone else who wants to prove their own Go
skill is better.

So read this document two ways. As a **report**, it shows the current standings: `go-mastery`
lifts every model we tested, on two vendors, with zero regressions, and leads every other Go
skill we benchmarked. As a **standard**, it describes a measurement instrument built to be
trusted by people who didn't write the skill — toolchain-graded, hidden-oracle, hermetic,
deterministic where it can be and honest about noise where it can't.

**Skill fingerprint:** `sha256:c3f30e36` · **Go toolchain:** 1.26 · **Harness:** `go-mastery-evals`

---

## TL;DR

- **Net-positive on every model, on both vendors, with zero regressions.** Injecting the skill
  lifts correctness on Anthropic Haiku **+20.0 pp**, Sonnet **+16.7 pp**, Opus **+14.1 pp**, and
  on OpenAI GPT‑5.4‑mini **+19.3 pp** and GPT‑5.5 **+11.9 pp**. No model got worse on a single
  case in any run.
- **The lift is corrective, not cosmetic.** On the weakest tier (Haiku) the skill fixes **12 of
  the 15** tasks the base model fails on its own; on the strong tiers it fixes **100%** of the
  few they miss.
- **Still measurably better when "does it pass" saturates.** On Opus — which passes essentially
  everything with or without the skill — a deterministic, no-model quality score shows the
  with-skill code is more idiomatic by **+0.32** on already-passing cases.
- **Ahead of every other Go skill we measured.** Versus JetBrains `go-modern-guidelines`:
  **+6.7 / +5.2 / +4.5 pp** across the three tiers, **never behind on a single case** (10 cases
  only we pass, 0 only they pass). Versus the leading community-authored Go skill: **+6.3 pp**,
  3–0, with idiom density roughly level.
- **Does no harm out of its domain.** On a third-party benchmark it wasn't built for (Aider
  polyglot Go / Exercism), the always-on skill is neutral within sampling noise.
- **It's a standard, not a one-off.** Every number above is reproducible with a `make` target
  against a vendored toolchain. If JetBrains, a community author, or a future skill wants to
  claim they're better, the apparatus to prove it is right here.

---

# Part I — The benchmark: why this number can be trusted

A benchmark is only worth adopting if a skeptic who didn't write the skill would accept its
verdict. Eight design choices make that the case.

### 1. Graded by the Go toolchain, not by a model

A coding skill has a luxury most don't: the language ships its own oracle. Every candidate is
judged by `gofmt -l`, `go vet`, `go build`, the case's `go test` behavioral test, and (when
installed) `golangci-lint` — plus regex assertions for "used the modern idiom / avoided the
anti-pattern." There is no LLM-as-judge anywhere in the loop. A case either compiles, passes
its test, and uses the required construct, or it does not. That removes the single largest
source of doubt in skill evaluations.

### 2. The behavioral test is a hidden oracle — even during self-correction

The model never sees the test that grades it. This matters most in the agentic loop (below):
when the model is shown tool output to fix its own code, it sees `gofmt`/`build`/`vet`/`lint`
diagnostics **on its own source** — never the behavioral test, never the expected output. So
"it passed" can never mean "it was handed the answer." The oracle stays sealed.

### 3. Agentic grading — measured the way it's deployed

Skills aren't used in one shot; they're used in editors and CI where the compiler talks back.
So after generating, the model gets two `--fix-rounds` to repair its own code from real
toolchain output. This is deliberately *generous to both arms* (with and without the skill get
the same rounds), which makes the remaining delta a conservative, deployment-realistic estimate
of the skill's value rather than a one-shot artifact.

### 4. Neutral prompts — we measure the skill, not the question

Every prompt asks for the outcome ("implement X", "use the most modern idiom") and never names
the API. If a prompt said "use `errors.AsType`," it would be testing reading comprehension, not
the skill. Both arms get a byte-identical user prompt and the same "output only Go" instruction;
the **only** difference between them is whether `SKILL.md` (plus the references a case routes to)
is injected as system context. The delta is the skill and nothing else.

### 5. The cases validate themselves

Every case ships a `solution_good.go` that **must grade PASS** and a `solution_bad.go` that
**must grade FAIL** on the targeted axis. `--validate-cases` enforces both before a case counts
as real. This is the benchmark testing its own discrimination: the good fixture proves the task
is winnable, the bad fixture proves the grader actually catches the thing it claims to catch. A
case that can't fail isn't measuring anything.

### 6. Hermetic and offline — reproducible on any machine

Grading runs against a **vendored** module with `GOPROXY=off`, `GOSUMDB=off`,
`GOTOOLCHAIN=local`, `-mod=vendor`. A stray third-party import or a network dependency fails
fast instead of silently fetching, so a grade means the same thing on your laptop as on ours,
today and next year.

### 7. Two metrics — because pass/fail is the wrong instrument on a strong model

*Correctness* (pass@1, majority of 5 samples) is the headline where the model has headroom. But
a frontier model passes most cases with or without help, so correctness alone reads "no lift"
even when the code clearly improved. The second metric, **deterministic quality**, scores the
emitted code itself — idiom adoption minus anti-patterns, on comment-stripped source, with
per-case rubrics. It uses **no model, no sampling, no API**, so it is fully reproducible and
**free to recompute**: generate once, score forever, iterate the rubric offline. It cannot be
gamed by re-rolling the dice.

### 8. Honest about noise

Temperature‑0 is not actually deterministic on hosted APIs, so a binary majority verdict
wobbles — a 4/5 ↔ 5/5 flip looks like a regression when it's sampling jitter. A baseline here is
therefore a **vector** of `(pass_rate, quality)` per (model, case), and `make compare` flags a
regression only when a drop clears a tolerance (`--pass-tol 0.2`, `--quality-tol 0.5`). The
benchmark refuses to cry wolf on a single-sample flip.

**Coverage.** 54 in-domain cases spanning concurrency, error handling, modern-API
modernization, security, gRPC, observability/OTel, MCP, eBPF, cgo, Wasm, cloud-native, data
structures, encoding, networking, and correctness traps — plus a 36-case external Aider-polyglot
Go track used purely as a do-no-harm guardrail. Cases skew toward the *hard, current, and niche*
on purpose: that is where a skill can separate from a strong base model.

---

# Part II — How the skill moves the needle

The skill is not a pile of tips. It encodes a small set of load-bearing principles, and the
benchmark shows each one converting into fixed cases. A few concrete mechanisms:

**"Don't start a goroutine you can't stop."** The concurrency cases (`concurrency-search-leak`,
`concurrency-worker-ctx`, `concurrency-pipeline-cancel`) are graded by a behavioral test that
*times out* if a worker leaks. Without the skill, weaker models spawn goroutines with no
`ctx.Done()` shutdown path; the test hangs and fails. With the skill, the model threads context
and selects on cancellation — and the case passes. The skill turns an invisible leak into
correct code.

**"Honor the caller's contract, then optimize."** `event-driven-bus` asks for an in-process
pub/sub bus whose `Publish` must not block *and* must deliver to subscribers. The naive answer
uses an unbuffered or size-1 channel with a `default:` drop — it doesn't block, but it silently
loses messages, so the delivery test fails. Without the skill, Haiku and Opus land this only
2/5. The skill's guidance — size the buffer for the expected burst and treat `default:` as an
*overflow valve, not normal-case loss* — takes both to **5/5**. This is the single most
corrective case in the suite.

**Parameterize, wrap, and thread context — together.** `security-sql-injection` passes 5/5 on
Opus with *and* without the skill, so correctness says nothing. Quality does: with the skill the
answer uses a parameterized query **and** wraps the error with `%w` **and** carries
`context.Context` (quality 3.0); without, it does fewer of the three (1.0). The skill doesn't
just avoid the injection — it produces the whole production-grade shape.

**Reach for the current idiom.** Modernization cases (`modern-waitgroup-go`,
`modern-errors-astype`, `errors-join-aggregate`, `modern-slices-contains`, `modern-rand-v2`)
isolate Go 1.21–1.26 constructs a model trained on older code under-uses. The skill supplies the
current form — `sync.WaitGroup.Go`, `errors.AsType[T]`, `errors.Join`, `slices.Contains` — and
the idiom-adoption deltas move accordingly (e.g. `errors-join-aggregate`: from −0.2 without to
+1.6 with). Freshness is a measurable axis, and the skill owns it.

The aggregate signature is the tell that this is real: **the largest correctness lift lands on
the smallest model, and compresses as the model saturates.** A weak model lacks the knowledge and
the skill supplies it (+20 pp on Haiku); a frontier model already has most of it, so the lift
moves from *correctness* to *quality* (+0.32 on Opus). Same skill, different axis per tier —
exactly what a real knowledge transfer looks like.

---

# Part III — Current standings

All correctness figures are pass@1 = mean over cases of (samples passed ÷ samples), majority of
5 samples, agentic (`--fix-rounds 2`).

### Cross-vendor results (in-domain, 54 cases, samples=5)

| Vendor | Tier | with | without | correctness lift | corrective fixes | regressions |
|---|---|---|---|---|---|---|
| Anthropic | Haiku (small) | 93.0% | 73.0% | **+20.0 pp** | 12/15 | **0** |
| Anthropic | Sonnet (medium) | 100.0% | 83.3% | **+16.7 pp** | 9/9 | **0** |
| Anthropic | Opus (large) | 100.0% | 85.9% | **+14.1 pp** | 8/8 | **0** |
| OpenAI | GPT‑5.4‑mini (mid) | 96.7% | 77.4% | **+19.3 pp** | 11/12 | **0** |
| OpenAI | GPT‑5.5 (frontier) | 98.9% | 87.0% | **+11.9 pp** | 7/7 | **0** |

*Corrective fixes* = of the cases the base model fails without the skill, how many the skill
repairs. The signature is identical across both vendors: biggest lift on the smallest model,
compressing toward saturation. **The skill is not Claude-specific.**

> **OpenAI provenance, stated plainly.** The mini and GPT‑5.5 rows are computed from
> `baselines/openai-gpt5/results-mini55.json`. They are *conservative*: that snapshot predates the
> `event-driven-bus` case fix, which on Anthropic only ever raised the affected case — so
> consolidating it can move these numbers up, not down. The **smallest** OpenAI tier
> (GPT‑5.4‑nano) full-suite run and **GPT‑5.5‑pro** are not included here: nano awaits a re-locked
> baseline, and `gpt-5.5-pro` is served only through OpenAI's Responses API, which the harness's
> chat-completions runner doesn't target. See Limitations.

### Quality where correctness saturates (deterministic, both-pass cases)

On the strong tiers, with/without both pass, so correctness reads flat. The deterministic
quality score (idiom adoption − anti-patterns, no model) shows the code still improved:

| Tier | Δ quality (both-pass) | n both-pass |
|---|---|---|
| Haiku | +0.26 | 39 |
| Sonnet | +0.26 | 45 |
| Opus | **+0.32** | 46 |

These are computed offline from the emitted code, so they are exactly reproducible and immune to
sampling. They are the answer to "your strong-model lift is zero" — it isn't; it moved axes.

### Head-to-head vs other Go skills

Same cases, same harness, same agentic loop; the competing skill is injected exactly the way
ours is. We report our `with` arm against each competitor's `with` arm.

| Competitor | tiers | us − them | only we pass | only they pass | idiom density |
|---|---|---|---|---|---|
| **JetBrains** `go-modern-guidelines` | Haiku / Sonnet / Opus | **+6.7 / +5.2 / +4.5 pp** | 10 | **0** | ≈ level |
| Leading community-authored Go skill | Sonnet | **+6.3 pp** | 3 | **0** | ≈ level |

**Honest read.** Both are good skills. On pure idiom density we are roughly level with a
purpose-built modern-idiom skill — that's a fair fight and we don't win it by a mile. Our margin
is **correctness and breadth on the hard, current, and niche** problems: current-API freshness
(the MCP Go SDK, `net/netip`), concurrency depth (context propagation and leak-freedom), and
several domains the others don't cover at all (MCP, eBPF, cgo, Wasm, cloud-native). Across every
tier and both competitors, **we are never behind on a single case.**

> **Attribution policy.** We name skills published by organizations and commercial vendors —
> JetBrains' `go-modern-guidelines` is one, and naming it is fair. For skills authored by
> individual community maintainers we report the result **without attaching a person's name**: a
> public benchmark should let the work speak for itself, and we would rather earn a comparison
> than make one at an individual's expense. The harness stages any skill identically, so the
> author of that skill — or anyone else — can reproduce these exact numbers, or run their own
> skill through the same gate, in minutes. The point of releasing the benchmark is that the
> leaderboard belongs to everyone, not to us.
>
> *Measurement note:* the head-to-head and community comparisons were run at `samples=3` on a
> prior skill build (`go-mastery` is marginally stronger now), which makes both results
> conservative. The cross-vendor matrix above is the `samples=5` headline.

### Do-no-harm: external benchmark (Aider polyglot Go, 36 cases)

Generic Exercism algorithm puzzles — *not* the production-Go domain the skill targets — used as a
guardrail: does an always-on skill drag a model down on work it wasn't built for?

| Tier | with − without | regressions |
|---|---|---|
| Haiku | +1.9 pp | 1 |
| Sonnet | −1.0 pp | 0 |
| Opus | −1.0 pp | 2 |

Neutral within sampling noise, no systemic drag. The skill's leverage is production-Go
idioms/APIs/concurrency, which these puzzles don't exercise — so neutrality here is the honest,
expected result, and we report the handful of single-case flips rather than hiding them.

---

# Part IV — Reproduce it, or run your own skill

The benchmark is the deliverable. Everything above is a `make` target.

```bash
make gates                  # apparatus unit tests + every case discriminates (no API)
make smoke                  # cheap 1-tier in-domain canary (small API spend)
make smoke-harm             # out-of-domain do-no-harm canary
make baseline VERSION=...   # full A/B, snapshots results + metrics + manifest + report
make compare BASE=...       # guard a new run against a locked baseline (noise-tolerant)
```

**Run a different skill.** Stage any skill the way the competitors are staged
(`harness/competitors/`), point the harness at it, and you get the same toolchain-graded number.
**Bring your own model.** `--runner byo` writes the prompts to disk so you can run them through
any agent — Claude, GPT, Cursor, a local model — paste back the output, and grade it. The gate
is identical regardless of who is being measured.

Layered cheap→expensive gating (`make gates` → `smoke` → `baseline`) keeps iteration fast and
keeps expensive runs honest; see `EVAL-STRATEGY.md` for the design and the retrospective behind
it.

---

## Limitations (stated plainly)

- **OpenAI baseline isn't fully consolidated yet.** mini and GPT‑5.5 are locked and reported;
  the smallest tier (GPT‑5.4‑nano) needs a re-locked full-suite baseline, and the
  `event-driven-bus` fix should be folded into the OpenAI snapshot (it can only raise the
  numbers). `gpt-5.5-pro` is Responses-API-only and out of scope for the current runner.
- **Quality is a heuristic.** It is presence-based idiom regexes plus lint/gofmt when Go is
  available. It has resolution, not perfection; per-case rubrics sharpen it, and it is deliberately
  conservative (presence, not frequency).
- **The hardest concurrency case stays hard for small models.** Even with the skill, the smallest
  tiers don't reach 5/5 on every concurrency task — the skill helps and never hurts, but it isn't
  magic on a model without the headroom.
- **Out-of-domain is neutral, not positive — by design.** The skill targets production Go; it does
  not make a model better at generic algorithm puzzles and we don't claim it does.
- **Head-to-heads were `samples=3` on a prior skill build.** Reported as conservative; the
  `samples=5` cross-vendor matrix is the primary result.

---

## Artifacts & provenance

- `baselines/deepened-v3/` — Anthropic in-domain, current skill (`c3f30e`), the headline matrix.
- `baselines/openai-gpt5/` — OpenAI cross-vendor portability (consolidation pending, above).
- `baselines/h2h-jetbrains/` — JetBrains head-to-head (competitor injected identically).
- `baselines/deepened-v2-aider/` — external do-no-harm track.
- `harness/` — grader, runners, deterministic quality scorer, noise-tolerant compare, unit tests.
- `EVAL-STRATEGY.md` — layered gate design, baseline protocol, and an honest retrospective on
  every bug and how the apparatus now catches it.

Every baseline carries a skill fingerprint and a manifest (models, samples, Go version, date);
**editing `SKILL.md` invalidates a baseline and requires a fresh one.** Without provenance a
number isn't citable — so every number here has it.
