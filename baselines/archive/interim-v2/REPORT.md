# Go Mastery — Eval Report (cross-model)

## Provenance

- **Models:** claude-haiku-4-5-20251001, claude-sonnet-4-6, claude-opus-4-8
- **Runner:** anthropic
- **Temperature (requested):** 0.0
- **Samples / (case,variant):** 5
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:4a0234e6d65e (content)
- **Generated (UTC):** 2026-06-25 18:00:34Z

## Cross-model matrix

Corrective = of cases the base model fails *without* the skill, the fraction the skill fixes. Regressions = passed *without* but failed *with* (want 0).

| Model | cases | with pass@1 | without pass@1 | lift | corrective | regressions |
|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | 22 | 91% | 68% | +22.7 pp | 5/7 (71%) | 0 |
| claude-sonnet-4-6 | 22 | 95% | 84% | +11.8 pp | 4/4 (100%) | **1** ⚠️ |
| claude-opus-4-8 | 22 | 98% | 95% | +3.6 pp | 1/1 (100%) | 0 |

### ⚠️ Regressions detected (skill made the base model worse)
- **claude-sonnet-4-6**: correctness-json-number

## Per-model detail

- **claude-haiku-4-5-20251001** → [`REPORT-claude-haiku-4-5-20251001.md`](REPORT-claude-haiku-4-5-20251001.md)
- **claude-sonnet-4-6** → [`REPORT-claude-sonnet-4-6.md`](REPORT-claude-sonnet-4-6.md)
- **claude-opus-4-8** → [`REPORT-claude-opus-4-8.md`](REPORT-claude-opus-4-8.md)
