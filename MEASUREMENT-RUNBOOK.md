# Measurement runbook — deepened skill vs locked baseline

How to measure the impact of the deepened references on **your machine** (the A/B run
calls Haiku/Sonnet/Opus, so it needs an API key — it cannot run in the sandbox).

## What is already validated (offline, no key)

- **All 30 cases discriminate**: every case ships a `solution_good.go` that PASSES the
  grader and a `solution_bad.go` that FAILS it. Confirmed via the harness:
  `python3 run_evals.py --validate-cases` → `VALIDATE-CASES (30 cases): PASS`.
- **6 new hard P0 cases** target the newly-deepened traps:
  `errors-join-aggregate` (errors.Join keeps each cause matchable),
  `concurrency-detach-context` (context.WithoutCancel), `security-html-escaping`
  (html/template auto-escaping), `performance-pool-reset` (sync.Pool reset),
  `observability-slog-redaction` (slog.LogValuer), `debugging-all-goroutine-stacks`
  (runtime.Stack(buf, true)).

## Prereqs

```bash
cd go-mastery-evals
python3 -m pip install -r requirements.txt -r requirements-api.txt   # pyyaml + anthropic
export ANTHROPIC_API_KEY=sk-ant-...        # required for --runner anthropic
# Go 1.26.x must be on PATH (the grader builds candidates offline with -mod=vendor)
```

## Step 1 — offline gates (fast, no key)

```bash
make gates          # = --validate-cases + --selftest + unit tests
```
Expect `VALIDATE-CASES (30 cases): PASS` and the selftest/unittests green.

## Step 2 — the A/B measurement (needs key)

Runs each case **with** and **without** the skill, `--samples 5` (majority vote),
across all three tiers. Opus ignores `temperature`; the runner handles that automatically.

```bash
# (a) Focused: just the 6 new hard cases — quickest signal on the deepenings
python3 run_evals.py --runner anthropic --samples 5 \
  --models claude-haiku-4-5-20251001,claude-sonnet-4-6,claude-opus-4-8 \
  --only errors-join-aggregate,concurrency-detach-context,security-html-escaping,performance-pool-reset,observability-slog-redaction,debugging-all-goroutine-stacks

# (b) Full suite: all 30 cases (the regression-safety check)
python3 run_evals.py --runner anthropic --samples 5 \
  --models claude-haiku-4-5-20251001,claude-sonnet-4-6,claude-opus-4-8
```

## Step 3 — read the results

- `results/REPORT.md` — cross-model matrix: `with pass@1 | without pass@1 | lift | corrective | regressions`,
  **plus** a `## Quality (deterministic)` table: `quality with | without | Δ (all) | Δ (both-pass) | n both-pass`.
- `results/REPORT-<model>.md` — per-case detail + a per-case quality table (idiom hits/misses).
- **Headline by tier:** Haiku/Sonnet — corrective rate + lift (they have headroom). **Opus —
  Δquality (both-pass)** is the headline: where pass/fail saturates, the deterministic quality
  delta on already-correct code is the signal. **Regressions must be 0.** Watch Haiku as the
  attention-dilution canary.
- **Quality, free + reproducible (no API):**
  ```bash
  make quality          # per-model Δquality (all cases, and both-pass cases)
  make quality-panel    # case ids with |Δquality|>0 — regenerate these on Opus via --only
  ```
  Quality is scored from `results/raw` — generate once, score forever; re-run free after any
  rubric change. The `golangci-lint`/gofmt composite dimensions fold in when those tools are
  present and skip gracefully when they aren't.

## Step 4 — compare to the locked baseline

The pre-deepening baseline is in `baselines/definitive/`. Prior locked numbers (from
`EVALUATIONS.md`): Haiku +28.3pp, Sonnet +26.7pp, Opus +12.5pp, **0 regressions**, 24 cases.

`make compare` is **noise-tolerant** — a baseline is a `(pass_rate, quality)` vector, and a
single-sample (4/5↔5/5) flip is *within tolerance*, not a regression. It fails (exit 1) only
on a **correctness** drop `> --pass-tol` (default 0.2) or a **quality** drop `> --quality-tol`
(default 0.5) on a case that still passes.

```bash
make compare BASE=definitive          # tolerances default to 0.2 / 0.5
# tighten/loosen: make compare BASE=definitive PASS_TOL=0.3 QUALITY_TOL=0.5
```

(Old baselines without a `baseline-metrics.json` and without kept `raw/` compare on
pass-rate only; quality is simply skipped for them — no crash.)

## Step 5 — promote (only if clean)

If lift holds and regressions are 0, snapshot the run as the new locked baseline. `make baseline`
also writes `baseline-metrics.json` (the `(pass_rate, quality)` vector `compare` needs):

```bash
make baseline VERSION=deepened-v1     # REPORT*, results.json, baseline-metrics.json, MANIFEST.txt
```

Then update `EVALUATIONS.md` with the new numbers.

## Agentic self-correct mode (`--fix-rounds`)

Single-shot grading asks the model to hand-produce perfectly-formatted, import-clean
code with no tools — stricter than any real deployment, where the model runs
`gofmt`/`go build` and fixes its own output. `--fix-rounds N` reproduces deployment: after
generating, the harness runs **gofmt / go build / go vet / golangci-lint on the model's own
code**, feeds back any failures, and lets the model fix across up to `N` rounds before final
grading. **The hidden behavioral test is never shown** — it stays the grading oracle, so the
model can fix mechanical issues (formatting, unused imports) but cannot see or game the test.

```bash
# deployment-faithful: model self-corrects gofmt/build/vet/lint on its own code (2 rounds)
python3 run_evals.py --runner anthropic --samples 5 --fix-rounds 2 \
  --models claude-haiku-4-5-20251001,claude-sonnet-4-6,claude-opus-4-8
```

Report **both** for the fullest picture, nothing hidden:
- `--fix-rounds 0` (default) — strict single-shot raw output; surfaces mechanical-hygiene
  slips (the 4 documented regressions).
- `--fix-rounds 2` — how the skill actually performs in an agentic/editor/CI workflow; the
  mechanical slips self-correct, isolating the skill's substantive contribution.

`results.json` records `fix_rounds` (provenance) and `fix_rounds_used` per sample.

## Cross-vendor (OpenAI reasoning models + Google Gemini)

The skill is a system-prompt injection and grading/quality run only on the emitted Go, so
the A/B is **vendor-neutral** — only the runner changes. The OpenAI-compatible runner drives
OpenAI (incl. reasoning models), Gemini (its OpenAI-compat endpoint), OpenRouter, or a local
server with no extra dependency. Portability here is the point: if the skill lifts GPT and
Gemini too, it's a real skill, not Claude-overfit.

3-case smoke per vendor (in-domain canary span):

```bash
# OpenAI reasoning model (param quirks — max_completion_tokens swap, temperature strip — auto-handled)
OPENAI_API_KEY=… python3 run_evals.py --runner openai --model o4-mini --samples 1 \
  --fix-rounds 2 --variants with,without --only errors-join-aggregate,mcp-current-sdk,security-sql-injection

# Gemini (preset Google base_url + GEMINI_API_KEY; --model overrides the default gemini-2.5-pro)
GEMINI_API_KEY=… python3 run_evals.py --runner gemini --model gemini-2.5-pro --samples 1 \
  --fix-rounds 2 --variants with,without --only errors-join-aggregate,mcp-current-sdk,security-sql-injection
```

Other OpenAI-compatible endpoints reuse the same runner:

```bash
# Any OpenAI-compatible server (OpenRouter, vLLM, Ollama, …)
python3 run_evals.py --runner openai --base-url https://openrouter.ai/api/v1 \
  --api-key-env OPENROUTER_API_KEY --model <vendor/model> ...
```

The report, `make quality`, and `make compare` are **identical across vendors** (the metric
is vendor-neutral) — rows are tagged by `runner.model`, so cross-vendor lift, quality delta,
and per-tier discriminators are read exactly like the Anthropic runs. Param quirks are learned
and cached per run: a 400 telling you to use `max_completion_tokens`, or that a reasoning model
rejects `temperature`, is handled automatically (and the completion-tokens path uses a generous
cap so reasoning tokens don't truncate the answer).
