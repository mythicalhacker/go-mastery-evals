# Competitor skills (for the head-to-head)

Other Go skills are injected as the `competitor` variant (`--competitor-dir`) so we can
A/B our skill against theirs on the same cases, the same way ours is injected.

**Competitors are fetched and staged locally — not vendored here.** This directory ships
only the staging *scripts* and `PROVENANCE.md`; the third-party skill content is
git-ignored, so our repository redistributes none of it. See `PROVENANCE.md` for each
competitor's upstream URL, commit, license, and author credit.

## Stage a competitor

- **JetBrains `go-modern-guidelines`** (single-file): fetch its `SKILL.md` from the
  upstream in `PROVENANCE.md` into `jetbrains-go-modern/SKILL.md`. Then run the
  head-to-head:

  ```bash
  make h2h COMPETITOR=harness/competitors/jetbrains-go-modern
  ```

- **Community multi-skill plugin**: clone the upstream in `PROVENANCE.md` into
  `_community-src/`, then bridge it into our one-core + routed-references layout:

  ```bash
  git clone --depth 1 <upstream from PROVENANCE.md> harness/competitors/_community-src
  python3 harness/competitors/stage_community.py     # writes ./community-go/
  make h2h COMPETITOR=harness/competitors/community-go
  ```

## Fairness mapping (how a multi-skill plugin is bridged)

A multi-skill competitor exposes many atomic skills loaded on demand; our injection
expects one always-on `SKILL.md` plus per-case routed `references/`. `stage_community.py`
bridges the two so the comparison steelmans the competitor:

- **Always-on core** = the competitor's foundational code-style/conventions skill,
  injected on every case — the analog of our always-on `SKILL.md`.
- **Per-case routing** = the competitor's single best-matching skill for each of our
  reference topics, with that skill's *own* `references/` included (its full topical
  depth). 21 of our 27 reference topics map to a competitor skill.
- **No-coverage topics** (`ai-ml-beyond-llm`, `cgo-and-interop`, `cloud-native`, `ebpf`,
  `mcp-and-agents`, `wasm-and-embedded`) are left unmapped on purpose: the competitor has
  no equivalent skill, so those cases get the core only. That is the honest representation
  of its catalog — and where our skill's differentiators show.

The same harness stages any skill identically, so the author of a competitor skill — or
anyone else — can reproduce these numbers, or run their own skill through the same gate.
