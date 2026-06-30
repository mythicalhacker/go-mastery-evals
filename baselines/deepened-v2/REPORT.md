# Go Mastery — Eval Report (cross-model)

## Provenance

- **Models:** claude-haiku-4-5-20251001, claude-sonnet-4-6, claude-opus-4-8
- **Runner:** anthropic
- **Temperature (requested):** 0.0
- **Samples / (case,variant):** 5
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:43293a4e71c8 (content)
- **Generated (UTC):** 2026-06-29 22:40:56Z

## Cross-model matrix

Corrective = of cases the base model fails *without* the skill, the fraction the skill fixes. Regressions = passed *without* but failed *with* (want 0).

| Model | cases | with pass@1 | without pass@1 | lift | corrective | regressions |
|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | 54 | 91% | 73% | +18.1 pp | 11/15 (73%) | 0 |
| claude-sonnet-4-6 | 54 | 100% | 83% | +16.7 pp | 9/9 (100%) | 0 |
| claude-opus-4-8 | 54 | 100% | 86% | +14.1 pp | 8/8 (100%) | 0 |

## Quality (deterministic)

Idiom adoption − anti-patterns on comment-stripped code (per-case rubrics; no API, fully reproducible). `both-pass` = each variant's pass-rate ≥ 0.6 — quality lift on already-correct code, the signal that survives when pass/fail saturates.

| Model | quality with | quality without | Δquality (all) | Δquality (both-pass) | n both-pass |
|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | +0.37 | +0.17 | +0.20 | +0.26 | 39 |
| claude-sonnet-4-6 | +0.43 | +0.22 | +0.21 | +0.26 | 45 |
| claude-opus-4-8 | +0.43 | +0.26 | +0.17 | +0.32 | 46 |

## Per-model detail

- **claude-haiku-4-5-20251001** → [`REPORT-claude-haiku-4-5-20251001.md`](REPORT-claude-haiku-4-5-20251001.md)
- **claude-sonnet-4-6** → [`REPORT-claude-sonnet-4-6.md`](REPORT-claude-sonnet-4-6.md)
- **claude-opus-4-8** → [`REPORT-claude-opus-4-8.md`](REPORT-claude-opus-4-8.md)
