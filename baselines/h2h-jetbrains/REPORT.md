# Go Mastery — Eval Report (cross-model)

## Provenance

- **Models:** claude-haiku-4-5-20251001, claude-sonnet-4-6, claude-opus-4-8
- **Runner:** anthropic
- **Temperature (requested):** 0.0
- **Samples / (case,variant):** 5
- **Go toolchain:** go version go1.26.0 darwin/arm64
- **Skill fingerprint:** sha256:43293a4e71c8 (content)
- **Generated (UTC):** 2026-06-30 10:05:31Z

## Results

_Only one variant present; need both `with` and `without` for lift._

## Quality (deterministic)

Idiom adoption − anti-patterns on comment-stripped code (per-case rubrics; no API, fully reproducible). `both-pass` = each variant's pass-rate ≥ 0.6 — quality lift on already-correct code, the signal that survives when pass/fail saturates.

| Model | quality with | quality without | Δquality (all) | Δquality (both-pass) | n both-pass |
|---|---|---|---|---|---|
| claude-haiku-4-5-20251001 | +0.38 | +0.17 | +0.21 | +0.00 | 0 |
| claude-sonnet-4-6 | +0.42 | +0.22 | +0.19 | +0.00 | 0 |
| claude-opus-4-8 | +0.44 | +0.26 | +0.19 | +0.00 | 0 |

## Per-model detail

- **claude-haiku-4-5-20251001** → [`REPORT-claude-haiku-4-5-20251001.md`](REPORT-claude-haiku-4-5-20251001.md)
- **claude-sonnet-4-6** → [`REPORT-claude-sonnet-4-6.md`](REPORT-claude-sonnet-4-6.md)
- **claude-opus-4-8** → [`REPORT-claude-opus-4-8.md`](REPORT-claude-opus-4-8.md)
