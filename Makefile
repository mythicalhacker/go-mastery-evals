# Eval harness — layered pipeline. Each layer is cheaper than the next and gates
# it: run L0/L1 (free) constantly, L2 (cheap) before any baseline, L3 (expensive)
# only when the cheap layers are green. See EVAL-STRATEGY.md for the rationale.

# Vendor the allowed golang.org/x/* deps into the grader's template module. Needs
# network ONCE; thereafter the grader builds candidates offline with -mod=vendor.
.PHONY: vendor
vendor:
	cd harness/_gomod_template && go mod tidy && go mod vendor
	@echo "Vendored. Commit harness/_gomod_template/{go.mod,go.sum,vendor/}."

# ----------------------------------------------------------------------------
# L0 + L1 — apparatus + case validation. Seconds to ~2 min. NO API key.
#   L0 unit tests exercise the grader's toolchain-integration layer (package
#   normalization, non-UTF-8 decode, build-vs-test, files/) — the layer where
#   every late bug lived. L1 proves each case discriminates (good PASS / bad FAIL).
# ----------------------------------------------------------------------------
.PHONY: gates
gates:
	python3 -m unittest discover -s tests
	python3 run_evals.py --selftest
	python3 run_evals.py --validate-cases

# External track validation (run after harness/external/stage_aider.py).
.PHONY: gates-aider
gates-aider:
	python3 run_evals.py --validate-cases --cases-dir cases-aider

# Quality (deterministic, NO API): scores idiom-adoption minus anti-patterns on
# the code already in results/raw, and the with-vs-without delta on both-pass cases.
# This is the metric for strong tiers (Opus), where behavioral pass/fail saturates.
# Generate once, score forever — re-run free after any rubric change.
.PHONY: quality
quality:
	python3 harness/quality.py results/raw results/results.json

# Quality panel: the small set of cases with a non-zero with-vs-without quality delta
# in the latest run — the ones worth regenerating on a strong tier (Opus) via --only.
.PHONY: quality-panel
quality-panel:
	python3 harness/quality.py --panel results/raw results/results.json

# ----------------------------------------------------------------------------
# L2 — smoke + do-no-harm canary. Minutes, SMALL spend (1 tier, samples=1).
#   Catches crashes, gross regressions, and out-of-domain drag BEFORE a full run.
#   Haiku is the default tier: it's the attention-dilution canary (weakest first).
# ----------------------------------------------------------------------------
SMOKE_MODEL ?= claude-haiku-4-5-20251001

# In-domain canary: a span where the skill must help or hold.
CANARY ?= concurrency-detach-context,errors-join-aggregate,security-sql-injection,modern-errors-astype,mcp-current-sdk,correctness-slice-aliasing
.PHONY: smoke
smoke:
	python3 run_evals.py --runner anthropic --model $(SMOKE_MODEL) --samples 1 --fix-rounds 2 \
	  --variants with,without --only $(CANARY)
	@echo "Smoke (in-domain): require 0 regressions before a baseline."

# Do-no-harm canary: OUT-OF-DOMAIN, deterministic algorithm tasks (incl. the two
# that previously regressed). This is the gate that would have caught the aider
# drag cheaply. Requires: python3 harness/external/stage_aider.py first.
HARM_CANARY ?= aider-variable-length-quantity,aider-protein-translation,aider-matrix,aider-hexadecimal,aider-crypto-square,aider-two-bucket
.PHONY: smoke-harm
smoke-harm:
	python3 run_evals.py --runner anthropic --model $(SMOKE_MODEL) --samples 3 --fix-rounds 2 \
	  --variants with,without --cases-dir cases-aider --only $(HARM_CANARY)
	@echo "Smoke (do-no-harm): the skill must not drag any of these below baseline."

# ----------------------------------------------------------------------------
# L3 — full baseline. The expensive run; only after gates + smoke are green.
#   Usage: make baseline VERSION=deepened-v1
# ----------------------------------------------------------------------------
MODELS ?= claude-haiku-4-5-20251001,claude-sonnet-4-6,claude-opus-4-8
.PHONY: baseline
baseline:
	@test -n "$(VERSION)" || { echo "ERROR: set VERSION=<name>  (e.g. make baseline VERSION=deepened-v1)"; exit 1; }
	python3 run_evals.py --runner anthropic --samples 5 --fix-rounds 2 \
	  --variants with,without --models $(MODELS)
	mkdir -p baselines/$(VERSION)
	cp results/REPORT*.md results/results.json baselines/$(VERSION)/
	# Noise-tolerant metric vector (pass_rate + quality) so `compare` needs no kept raw.
	python3 harness/quality.py --dump-metrics results/raw results/results.json \
	  > baselines/$(VERSION)/baseline-metrics.json
	{ echo "version: $(VERSION)"; date -u +"generated: %Y-%m-%dT%H:%M:%SZ"; \
	  echo "models: $(MODELS)"; echo "samples: 5  fix_rounds: 2"; \
	  printf "skill_fingerprint: "; grep -h 'Skill fingerprint' results/REPORT.md | head -1; \
	  printf "git: "; (cd .. && git rev-parse --short HEAD 2>/dev/null || echo n/a); \
	  printf "go: "; go version; } > baselines/$(VERSION)/MANIFEST.txt
	@echo "Baseline saved -> baselines/$(VERSION)/  (REPORT*, results.json, MANIFEST.txt)"

# Guard: diff the latest results against a locked baseline. NOISE-TOLERANT — a
# single-sample (4/5<->5/5) flip is within tolerance; non-zero exit only on an
# out-of-tolerance correctness OR quality regression. Usage: make compare BASE=deepened-v1
PASS_TOL ?= 0.2
QUALITY_TOL ?= 0.5
.PHONY: compare
compare:
	@test -n "$(BASE)" || { echo "ERROR: set BASE=<name>"; exit 1; }
	python3 harness/compare_baseline.py baselines/$(BASE) results/results.json \
	  --pass-tol $(PASS_TOL) --quality-tol $(QUALITY_TOL)

# Head-to-head vs a competitor skill, injected as the `competitor` variant exactly the
# way ours is. Stage the competitor first (see harness/competitors/README.md + PROVENANCE.md);
# competitor content is fetched locally, never vendored here.
#   Usage: make h2h COMPETITOR=harness/competitors/jetbrains-go-modern
H2H_MODELS ?= claude-haiku-4-5-20251001,claude-sonnet-4-6,claude-opus-4-8
.PHONY: h2h
h2h:
	@test -n "$(COMPETITOR)" || { echo "ERROR: set COMPETITOR=<dir>  (e.g. harness/competitors/jetbrains-go-modern)"; exit 1; }
	python3 run_evals.py --runner anthropic --samples 5 --fix-rounds 2 \
	  --variants with,competitor --competitor-dir $(COMPETITOR) --models $(H2H_MODELS)
	mkdir -p baselines/h2h-$(notdir $(COMPETITOR))
	cp results/REPORT*.md results/results.json baselines/h2h-$(notdir $(COMPETITOR))/
	python3 harness/quality.py --dump-metrics results/raw results/results.json \
	  > baselines/h2h-$(notdir $(COMPETITOR))/baseline-metrics.json
	@echo "Head-to-head saved -> baselines/h2h-$(notdir $(COMPETITOR))/"
