# Go Mastery — Eval Report (cross-model)

## Provenance

- **Models:** claude-sonnet-4-6
- **Runner:** anthropic
- **Temperature (requested):** 0.0
- **Samples / (case,variant):** 3
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:24ef6b199646 (content)
- **Generated (UTC):** 2026-06-29 11:39:55Z

## Cross-model matrix

Corrective = of cases the base model fails *without* the skill, the fraction the skill fixes. Regressions = passed *without* but failed *with* (want 0).

| Model | cases | with pass@1 | without pass@1 | lift | corrective | regressions |
|---|---|---|---|---|---|---|
| claude-sonnet-4-6 | 53 | 100% | 83% | +17.0 pp | 9/9 (100%) | 0 |

## Head-to-head vs competitor skill

Our skill vs the competitor (`competitor` variant) on the same cases. `only we pass` / `only they pass` count cases one skill gets right and the other doesn't.

| Model | cases | our pass@1 | competitor pass@1 | us − competitor | only we pass | only they pass |
|---|---|---|---|---|---|---|
| claude-sonnet-4-6 | 53 | 100% | 94% | +6.3 pp | 3 | 0 |

## Per-model detail

- **claude-sonnet-4-6** → [`REPORT-claude-sonnet-4-6.md`](REPORT-claude-sonnet-4-6.md)
