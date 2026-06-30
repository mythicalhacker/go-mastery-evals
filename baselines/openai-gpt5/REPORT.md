# Go Mastery — Eval Report (cross-model)

## Provenance

- **Models:** gpt-5.4-mini, gpt-5.5
- **Runner:** openai
- **Temperature (requested):** 0.0
- **Samples / (case,variant):** 5
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:43293a4e71c8 (content)
- **Generated (UTC):** 2026-06-30 14:17:37Z

## Cross-model matrix

Corrective = of cases the base model fails *without* the skill, the fraction the skill fixes. Regressions = passed *without* but failed *with* (want 0).

| Model | cases | with pass@1 | without pass@1 | lift | corrective | regressions |
|---|---|---|---|---|---|---|
| gpt-5.4-mini | 54 | 97% | 77% | +19.3 pp | 11/12 (92%) | 0 |
| gpt-5.5 | 54 | 99% | 87% | +11.9 pp | 7/7 (100%) | 0 |

## Per-model detail

- **gpt-5.4-mini** → [`REPORT-gpt-5.4-mini.md`](REPORT-gpt-5.4-mini.md)
- **gpt-5.5** → [`REPORT-gpt-5.5.md`](REPORT-gpt-5.5.md)
