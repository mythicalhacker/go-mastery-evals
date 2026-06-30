# Competitor provenance & attribution

This benchmark compares `go-mastery` against other Go skills by injecting each as the
`competitor` variant on the same cases. **We redistribute none of that third-party
content.** This repository ships only the staging *scripts* and this provenance file; a
cloner fetches each competitor from its upstream and stages it locally (it is
git-ignored). This file is the correct place to credit each author and their license —
crediting their work, not competing with their name in our positioning copy.

## JetBrains — `go-modern-guidelines`

- **Author / owner:** JetBrains (commercial vendor).
- **Upstream:** https://github.com/JetBrains/go-modern-guidelines
  (skill at `claude/modern-go-guidelines/skills/use-modern-go/SKILL.md`).
- **What it is:** a single-file modern-Go guidelines skill.
- **Staged into:** `jetbrains-go-modern/SKILL.md` (git-ignored; fetch the file from the
  upstream path above).
- **License:** as stated in the upstream repository — see its `LICENSE`. We redistribute
  none of it; it is fetched and used locally only, for an A/B comparison.

## Community Go skill — `cc-skills-golang`

- **Author:** samber (Samuel Berthe) — https://github.com/samber
- **Upstream:** https://github.com/samber/cc-skills-golang
- **Staged from:** commit `466ea6dfd4aecb5c19caf29e7595e752c66c1a5d` (2026-06-23).
- **What it is:** a multi-skill plugin of many atomic Go skills (on-demand). Our harness
  expects one always-on `SKILL.md` plus per-case routed `references/`, so
  `stage_community.py` bridges its layout into ours for a fair head-to-head (see that
  script and `README.md` for the exact, steelmanned mapping).
- **Staged into:** `community-go/` (git-ignored), from a local clone at `_community-src/`.
- **License:** MIT. **All rights to that content remain with its author; we redistribute
  none of it** — only the staging script and this credit.

We thank both authors: their public work makes an apples-to-apples comparison possible,
and the same harness lets either of them (or anyone) reproduce these numbers or run their
own skill through the identical gate.
