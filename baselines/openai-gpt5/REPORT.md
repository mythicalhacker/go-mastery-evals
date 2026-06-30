# Go Mastery — Eval Report (cross-model)

## Provenance

- **Models:** gpt-5.4-nano, gpt-5.4-mini, gpt-5.5
- **Runner:** openai
- **Temperature (requested):** 0.0
- **Samples / (case,variant):** 5
- **Skill fingerprint:** sha256:c3f30e363f88 (content)

## Cross-model matrix

Corrective = of cases the base model fails *without* the skill, the fraction the skill fixes. Regressions = passed *without* but failed *with* (want 0).

| Model | cases | with pass@1 | without pass@1 | lift | corrective | regressions |
|---|---|---|---|---|---|---|
| gpt-5.4-mini | 54 | 99% | 78% | +20.7 pp | 12/12 (100%) | 0 |
| gpt-5.5 | 54 | 100% | 87% | +12.6 pp | 7/7 (100%) | 0 |
| gpt-5.4-nano | 54 | 94% | 67% | +26.3 pp | 15/17 (88%) | 0 |

## Per-model detail

- **gpt-5.4-mini** → [`REPORT-gpt-5.4-mini.md`](REPORT-gpt-5.4-mini.md)
- **gpt-5.5** → [`REPORT-gpt-5.5.md`](REPORT-gpt-5.5.md)
- **gpt-5.4-nano** → [`REPORT-gpt-5.4-nano.md`](REPORT-gpt-5.4-nano.md)
