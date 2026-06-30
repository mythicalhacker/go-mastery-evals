#!/usr/bin/env python3
"""Stage a multi-skill community Go skill into a competitor dir mirroring our layout.

The community skill is a *multi-skill* competitor (many atomic, on-demand skills). Our
harness's competitor injection (runners.system_for) expects one always-on SKILL.md plus
references/<our-ref-name>.md routed per case. This script bridges the two so the
head-to-head is fair: on every case the competitor gets its single best-matching skill
(SKILL.md + that skill's own references/, i.e. its full topical depth), plus a light
always-on core. Where the competitor genuinely has no equivalent skill (mcp, ebpf, cgo,
cloud-native/k8s, wasm, ai/ml), the ref is intentionally left unmapped, so it gets the
core only — the honest representation of its coverage, and where our skill's moat shows.

The staged output (./community-go/) is NOT committed — it is third-party content we
redistribute none of. Provenance (upstream URL, commit, license, credit) is in
PROVENANCE.md; clone the upstream listed there into ./_community-src, then run this.

Usage:
    git clone --depth 1 <upstream from PROVENANCE.md> _community-src
    python3 stage_community.py        # writes ./community-go/{SKILL.md,references/*}
"""
from __future__ import annotations
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "_community-src" / "skills"
DST = HERE / "community-go"

# our reference name -> community skill giving the strongest topical match (steelman)
MAP = {
    "concurrency.md": "golang-concurrency",
    "modern-go.md": "golang-modernize",
    "data-structures-and-caching.md": "golang-data-structures",
    "errors-and-resilience.md": "golang-error-handling",
    "security.md": "golang-security",
    "style-synthesis.md": "golang-code-style",
    "database.md": "golang-database",
    "observability.md": "golang-observability",
    "cli-and-config.md": "golang-cli",
    "debugging-and-diagnostics.md": "golang-troubleshooting",
    "design-patterns.md": "golang-design-patterns",
    "advanced-patterns.md": "golang-design-patterns",
    "performance.md": "golang-performance",
    "internals.md": "golang-performance",
    "file-io.md": "golang-safety",
    "api-design.md": "golang-structs-interfaces",
    "http-and-apis.md": "golang-popular-libraries",
    "encoding-and-serialization.md": "golang-popular-libraries",
    "distributed-systems.md": "golang-grpc",
    "event-driven.md": "golang-design-patterns",
    "networking.md": "golang-popular-libraries",
}
# our refs with no community equivalent — left unmapped on purpose (competitor = core only)
NO_COVERAGE = [
    "ai-ml-beyond-llm.md", "cgo-and-interop.md", "cloud-native.md",
    "ebpf.md", "mcp-and-agents.md", "wasm-and-embedded.md",
]
CORE_SKILL = "golang-code-style"  # the competitor's foundational conventions = always-on core


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[text.find("\n", end + 1) + 1:].strip()
    return text.strip()


def _full_skill(name: str) -> str | None:
    d = SRC / name
    sk = d / "SKILL.md"
    if not sk.exists():
        return None
    parts = [f"# community skill: {name}\n\n" + _strip_frontmatter(sk.read_text())]
    refd = d / "references"
    if refd.is_dir():
        for r in sorted(refd.glob("*.md")):
            parts.append(f"\n\n## reference: {r.name}\n\n" + _strip_frontmatter(r.read_text()))
    return "\n".join(parts)


def main() -> None:
    if not SRC.is_dir():
        raise SystemExit(f"clone the upstream (see PROVENANCE.md) into {HERE/'_community-src'} first")
    (DST / "references").mkdir(parents=True, exist_ok=True)
    core = _full_skill(CORE_SKILL)
    (DST / "SKILL.md").write_text(core + "\n")
    print(f"core SKILL.md <- {CORE_SKILL} ({len(core.split())} words)")
    n = 0
    for ref, skill in MAP.items():
        c = _full_skill(skill)
        if c is None:
            print("  MISSING:", skill)
            continue
        (DST / "references" / ref).write_text(c + "\n")
        n += 1
    print(f"staged {n} routed references; no-coverage (core only): {', '.join(NO_COVERAGE)}")


if __name__ == "__main__":
    main()
