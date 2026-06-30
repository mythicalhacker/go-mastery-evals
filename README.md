# go-mastery-evals — the open benchmark for Go coding skills

Two things ship together: **`go-mastery`**, a skill that makes a model write production-grade,
idiomatic Go, and **`go-mastery-evals`** (this repo), the open harness that *measures* whether
any Go skill actually does that. The harness is the more durable contribution. A "best practices"
skill is a claim; this repository turns the claim into a number anyone can reproduce — and the
same number is available to anyone who wants to prove their own Go skill is better.

> **The skill this benchmarks → https://github.com/mythicalhacker/go-mastery**

It grades the output with the **Go toolchain itself** — `gofmt`, `go vet`, `go build`, `go test`,
`golangci-lint` — plus a **hidden behavioral test the model never sees**. No LLM-as-judge, no
vibes. A case compiles, passes its test, and uses the modern idiom, or it doesn't. Grading is
**hermetic** (vendored, offline) so a verdict means the same thing on your laptop as on ours.

- 📊 **Standings & full methodology → [RESULTS.md](RESULTS.md)** — per-tier tables, cross-vendor
  results, head-to-heads, do-no-harm track, limitations.
- 🧪 **Why the number can be trusted → [EVAL-STRATEGY.md](EVAL-STRATEGY.md)** — the layered gate
  design, baseline protocol, and an honest retrospective on every bug.
- 📣 **Launch copy → [RELEASE-BLURB.md](RELEASE-BLURB.md).**

The headline (see RESULTS.md for the rest): the skill lifts correctness **+12 to +26 pp on every
model of both Anthropic and OpenAI, with zero in-domain regressions**, and leads every other Go skill
benchmarked — and the harness ships so anyone can check, or try to beat it.

## Why toolchain-graded

For a *coding* skill the grader can be objective and cheap, because Go ships its own oracle:

- `gofmt -l` — is the model's file canonically formatted?
- `go vet ./...` — does it pass vet?
- `go build ./...` — does it compile?
- `go test ./...` — does it pass the case's **hidden** behavioral test? (The model never sees it,
  even during self-correction, so "it passed" can never mean "it was handed the answer.")
- `golangci-lint run` — default-on when installed (degrades to a skip when it isn't).
- `must_match` / `must_not_match` — did it use the modern idiom (e.g. `errors.AsType[`) and avoid
  the anti-pattern (e.g. `errors.As(`)?

A second, **deterministic quality** metric (idiom adoption − anti-patterns on comment-stripped
source, no model/API) catches improvement where pass/fail saturates on a strong model.

## Requirements

- **Go 1.26+** on `PATH` (the cases target 1.26 features). `go version` should work.
- **Python 3.9+** and `pip install -r requirements.txt` (PyYAML for the offline gates / BYO mode).
- Optional: `golangci-lint` (deepens linting), and the `anthropic` / `openai` SDKs for the
  automated runners (`pip install -r requirements-api.txt`).

## Quickstart

```bash
pip install -r requirements.txt

# Validate the harness itself — no API key, fully offline:
make gates                              # unit tests + every case discriminates (good PASS / bad FAIL)
python run_evals.py --list              # the cases

# Automated A/B (deterministic by default; --samples for rate-based lift):
pip install -r requirements-api.txt
export ANTHROPIC_API_KEY=sk-...         # or OPENAI_API_KEY / GEMINI_API_KEY
python run_evals.py --runner anthropic --model claude-sonnet-4-6 --samples 5 --fix-rounds 2

# Bring your own model (any agent — Claude, GPT, Gemini, Cursor, local):
python run_evals.py --runner byo        # writes prompts to outputs/prompts/<case>__<variant>.md;
                                        # run each, save replies to outputs/<case>__<variant>.go, re-run.
```

Results land in `results/REPORT.md` (cross-model matrix + per-case quality) and
`results/results.json`. The full `make` pipeline (`gates → smoke → baseline → compare`) is in the
[Makefile](Makefile); the design and baseline protocol are in [EVAL-STRATEGY.md](EVAL-STRATEGY.md)
and [MEASUREMENT-RUNBOOK.md](MEASUREMENT-RUNBOOK.md).

### Reproducibility knobs

- `--temperature` (default `0.0`), `--samples N` — the report shows pass *rate* per variant
  (macro **pass@1** = mean of per-case `k/N`) and computes **lift on rates**, not single shots.
- `--fix-rounds N` — agentic mode: the model repairs its own code from real `gofmt`/`build`/`vet`/
  `lint` output across N rounds (the hidden test is never shown). Deployment-faithful and generous
  to both arms, so the remaining delta is a conservative estimate of the skill's value.
- **Provenance** — every report records model id, temperature, samples, `go version`, a skill
  fingerprint, case count, and a UTC timestamp. Editing `SKILL.md` invalidates a baseline.
- **Offline & deterministic grading** — `GOPROXY=off`, `GOSUMDB=off`, `GOTOOLCHAIN=local`,
  `-mod=vendor`: a stray third-party import or network dependency fails fast instead of fetching.

## How the A/B is kept honest

For every case both variants get a **byte-identical** user prompt and the same "output only Go"
instruction. The prompt asks for the outcome ("implement X", "use the most modern idiom") and
**never names the API** — naming it would test reading comprehension, not the skill. The **only**
difference between the arms:

- **without** — neutral system prompt only.
- **with** — the skill is injected as system context: `SKILL.md` plus any `skill_refs` the case
  routes to (mirroring how an index would lazy-load those references).

So the delta is the skill and nothing else. A third arm, **competitor**, injects another skill the
same way for head-to-heads (see `harness/competitors/`).

## Adding a case

One directory per case under `cases/`:

```
cases/<id>/
  case.yaml          # metadata + grading rules
  prompt.md          # the task (identical for both variants; never names the API)
  test.go            # optional behavioral test, package solution (the hidden oracle)
  files/             # optional extra files copied into the temp module
  solution_good.go   # reference fixture that MUST grade PASS  (required)
  solution_bad.go    # reference fixture that MUST grade FAIL  (required)
```

`solution_good.go` / `solution_bad.go` are the case's own regression tests: the good one proves
the task is *winnable*, the bad one proves the grader actually *discriminates* (it must fail on the
targeted axis — wrong idiom, unsafe code, or a failing behavioral test). `--validate-cases` grades
both, and a case isn't "done" until the good passes and the bad fails. Keep the targeted pattern
out of fixture *comments* — `must_match`/`must_not_match` scan the whole file.

`case.yaml`:

```yaml
id: modern-errors-astype
title: Typed error extraction (errors.AsType)
category: modernization
go_version: "1.26"
filename: solution.go          # where the model's code is written
skill_refs: [modern-go.md]     # references injected in the "with" variant
checks:
  gofmt: true
  vet: true
  build: true
  test: true                   # runs the hidden test.go if present
  lint: true                   # golangci-lint when installed; skips gracefully otherwise
  must_match:    ['errors\.AsType\[']
  must_not_match: ['errors\.As\(']
```

A case **passes** only if every required check passes.

## Coverage

**54 in-domain cases** spanning concurrency (context propagation, leak-freedom, pipelines),
error handling, modern-API modernization (Go 1.22–1.26), security, gRPC, observability/OTel, MCP,
eBPF, cgo, Wasm, cloud-native, data structures, encoding, networking, and correctness traps —
plus a **36-case external Aider-polyglot Go track** used purely as a do-no-harm guardrail. Cases
skew toward the *hard, current, and niche* on purpose: that is where a skill separates from a
strong base model. See [RESULTS.md](RESULTS.md) for the full breakdown.

## Run your own skill — or bring your own model

The benchmark is the deliverable, and the leaderboard is meant to be public.

- **Run a different skill.** Stage any skill the way competitors are staged
  (`harness/competitors/` — fetched and staged locally, never vendored here; see
  [`harness/competitors/PROVENANCE.md`](harness/competitors/PROVENANCE.md) for attribution), point
  the harness at it with `--competitor-dir`, and you get the same toolchain-graded number. If you
  maintain a Go skill and think you can beat these numbers — `make baseline`, and prove it.
- **Bring your own model.** `--runner byo` writes the prompts to disk so you can run them through
  any agent — Claude, GPT, Gemini, Cursor, a local model — paste back the output, and grade it.
  The gate is identical regardless of who is being measured.

Attribution policy: we name commercial vendors (e.g. JetBrains) in comparisons; for skills by
individual community maintainers we report the result without attaching a person's name in
positioning copy, and credit them properly in
[`harness/competitors/PROVENANCE.md`](harness/competitors/PROVENANCE.md). The work speaks for
itself, and the harness lets anyone reproduce any comparison.

## License

MIT — see [LICENSE](LICENSE). Third-party competitor skills are **not** redistributed here; they
are fetched and staged locally, with attribution in `harness/competitors/PROVENANCE.md`.
