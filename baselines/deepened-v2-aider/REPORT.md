# Go Mastery — Eval Report (cross-model)

## Provenance

- **Models:** claude-haiku-4-5-20251001, claude-sonnet-4-6, claude-opus-4-8
- **Runner:** anthropic
- **Temperature (requested):** 0.0
- **Samples / (case,variant):** 3
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:43293a4e71c8 (content)
- **Generated (UTC):** 2026-06-30 00:39:22Z

## Cross-model matrix

Corrective = of cases the base model fails *without* the skill, the fraction the skill fixes. Regressions = passed *without* but failed *with* (want 0).

| Model | cases | with pass@1 | without pass@1 | lift | corrective | regressions |
|---|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | 36 | 14% | 12% | +1.9 pp | 2/32 (6%) | **1** ⚠️ |
| claude-sonnet-4-6 | 36 | 55% | 56% | -0.9 pp | 0/16 (0%) | 0 |
| claude-opus-4-8 | 36 | 58% | 59% | -0.9 pp | 1/15 (7%) | **2** ⚠️ |

### ⚠️ Regressions detected (skill made the base model worse)
- **claude-haiku-4-5-20251001**: aider-variable-length-quantity
- **claude-opus-4-8**: aider-food-chain, aider-zebra-puzzle

## Quality (deterministic)

Idiom adoption − anti-patterns on comment-stripped code (per-case rubrics; no API, fully reproducible). `both-pass` = each variant's pass-rate ≥ 0.6 — quality lift on already-correct code, the signal that survives when pass/fail saturates.

| Model | quality with | quality without | Δquality (all) | Δquality (both-pass) | n both-pass |
|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | +0.33 | +0.14 | +0.19 | +0.00 | 3 |
| claude-sonnet-4-6 | +0.37 | +0.18 | +0.19 | +0.05 | 20 |
| claude-opus-4-8 | +0.38 | +0.21 | +0.17 | +0.00 | 19 |

## Per-model detail

- **claude-haiku-4-5-20251001** → [`REPORT-claude-haiku-4-5-20251001.md`](REPORT-claude-haiku-4-5-20251001.md)
- **claude-sonnet-4-6** → [`REPORT-claude-sonnet-4-6.md`](REPORT-claude-sonnet-4-6.md)
- **claude-opus-4-8** → [`REPORT-claude-opus-4-8.md`](REPORT-claude-opus-4-8.md)
