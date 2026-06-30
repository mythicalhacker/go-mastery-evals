# External eval tracks

Third-party benchmarks wired into the harness for independent validation, separate
from our hand-authored `cases/`. These measure the skill against problems we did
**not** write — the credibility signal.

## Aider-polyglot — Go track

The Go exercises from the [Aider polyglot benchmark](https://github.com/Aider-AI/polyglot-benchmark)
(Exercism-format: instructions + stub + hidden tests + reference solution).

### Setup (not committed — regenerated locally)

```bash
cd harness/external
git clone --depth 1 https://github.com/Aider-AI/polyglot-benchmark _aider-src
python3 stage_aider.py                 # -> ../../cases-aider/aider-*
python3 ../../run_evals.py --validate-cases --cases-dir ../../cases-aider
```

`stage_aider.py` converts each exercise into our case format (driven by the
exercise's `.meta/config.json`):

- the exercise's own `*_test.go` is the grading oracle — **test-only**, the
  functional-correctness metric Aider/Exercism use (no gofmt/vet/lint here);
- the unimplemented stub becomes the prompt + `solution_bad.go`, the reference
  `.meta/example.go` becomes `solution_good.go`, so `--validate-cases` proves each
  case discriminates;
- `editor` scaffold files (interfaces, shared types, extra `cases_test.go`) are
  copied into `files/` so the package compiles;
- `skill_refs: []` — the `with` variant injects only the always-on `SKILL.md`, so
  this measures whether the skill **core** lifts general Go correctness.

39 exercises → **36 staged, 3 skipped** (recorded in `SKIP` with reasons): `counter`
(profiling exercise; stub is already complete), `ledger` and `markdown`
(refactoring exercises whose starting code already passes — `bad` can't FAIL).
All 36 validated: good→PASS, bad→FAIL.

`_aider-src/` and the generated `cases-aider/` are git-ignored (third-party content,
regenerable from the steps above).

### Run

```bash
# does the skill lift correctness on an external benchmark? (with vs without)
python3 run_evals.py --runner anthropic --samples 3 --fix-rounds 2 \
  --variants with,without --cases-dir cases-aider \
  --models claude-haiku-4-5-20251001,claude-sonnet-4-6,claude-opus-4-8
```
