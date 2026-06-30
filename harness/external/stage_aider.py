#!/usr/bin/env python3
"""Stage the Aider-polyglot Go exercises as an external eval track.

Reads harness/external/_aider-src/go/exercises/practice/* (Exercism layout) and
writes cases-aider/aider-<name>/ in our case format, so the existing harness can
grade the skill against a recognized third-party benchmark — independent of our
hand-authored cases.

Per exercise (driven by .meta/config.json):
  * solution[0]  -> the stub the model must implement  -> prompt + solution_bad.go
  * example[0]   -> .meta/example.go reference solution -> solution_good.go
  * every *_test.go physically present -> the grading oracle (first as test.go, the
    rest into files/ so they compile together)
  * other root .go (editor scaffold: interfaces.go, common.go, counter impls, ...)
    -> files/ (present for good/bad/model alike)

Grading is build+test only — functional correctness, the metric Aider/Exercism use
(no gofmt/vet/lint here; those are exercised by our own cases). skill_refs is empty,
so the `with` variant injects only the always-on SKILL.md — the honest "does the
skill core lift general Go correctness" measurement.

Usage:
    git clone --depth 1 https://github.com/Aider-AI/polyglot-benchmark _aider-src
    python3 stage_aider.py
    python3 ../../run_evals.py --validate-cases --cases-dir ../../cases-aider
"""
from __future__ import annotations
import json
import pathlib
import re
import shutil

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "_aider-src" / "go" / "exercises" / "practice"
DST = HERE.parent.parent / "cases-aider"

PKG_RE = re.compile(r"^\s*package\s+(\w+)", re.M)

# Exercises that don't fit the "implement the stub" mould — skipped with reason.
SKIP = {
    "counter": "stub ships a complete implementation (profiling exercise); bad==good, no discrimination",
    "ledger": "refactoring exercise — starting code already passes the tests; bad does not FAIL",
    "markdown": "refactoring exercise ('implementation to refactor') — stub already passes; bad does not FAIL",
}


def _pkg(text: str) -> str | None:
    m = PKG_RE.search(text)
    return m.group(1) if m else None


def _go_version(d: pathlib.Path) -> str:
    gm = d / "go.mod"
    if gm.exists():
        m = re.search(r"^go\s+(\S+)", gm.read_text(), re.M)
        if m:
            return m.group(1)
    return "1.22"


def stage_one(d: pathlib.Path):
    cfg = json.loads((d / ".meta" / "config.json").read_text()).get("files", {})
    sol, ex = cfg.get("solution", []), cfg.get("example", [])
    if len(sol) != 1 or len(ex) != 1:
        return ("skip", d.name, f"solution={sol} example={ex}")
    sol_file, ex_file = d / sol[0], d / ex[0]
    if not sol_file.exists() or not ex_file.exists():
        return ("skip", d.name, "missing solution/example file")
    good, bad = ex_file.read_text(), sol_file.read_text()
    pkg = _pkg(good) or _pkg(bad)
    if not pkg:
        return ("skip", d.name, "no package decl")
    tests = sorted(p for p in d.glob("*_test.go"))
    if not tests:
        return ("skip", d.name, "no tests")
    scaffold = [p for p in sorted(d.glob("*.go"))
                if p.name != sol_file.name and not p.name.endswith("_test.go")]

    cid = f"aider-{d.name}"
    out = DST / cid
    (out / "files").mkdir(parents=True, exist_ok=True)

    (out / "case.yaml").write_text(
        f"id: {cid}\n"
        f'title: "Aider polyglot: {d.name}"\n'
        f"category: aider-polyglot\n"
        f'go_version: "{_go_version(d)}"\n'
        f"package: {pkg}\n"
        f"filename: solution.go\n"
        f"skill_refs: []\n"
        # test-only: `go test` compiles the package *with* its test files, so it
        # subsumes a standalone build. build is set False explicitly because the
        # grader defaults it to True, and a standalone build wrongly fails when the
        # canonical solution uses a helper defined in the test file (bottle-song's Title).
        f"checks:\n  build: false\n  test: true\n"
    )

    instr = (d / ".docs" / "instructions.md").read_text()
    app = d / ".docs" / "instructions.append.md"
    if app.exists():
        instr += "\n\n" + app.read_text()
    parts = [
        instr.strip(),
        f"\n\n## Implement\n\nWrite the complete file `solution.go` in `package {pkg}` "
        f"implementing the stub below. Output exactly one Go code block.\n",
        f"\n```go\n{bad.strip()}\n```\n",
    ]
    if scaffold:
        parts.append("\n## Provided files (already present in the package — do not redefine):\n")
        for s in scaffold:
            parts.append(f"\n`{s.name}`:\n```go\n{s.read_text().strip()}\n```\n")
    (out / "prompt.md").write_text("".join(parts))

    shutil.copy(tests[0], out / "test.go")
    for t in tests[1:]:
        shutil.copy(t, out / "files" / t.name)
    for s in scaffold:
        shutil.copy(s, out / "files" / s.name)
    (out / "solution_good.go").write_text(good)
    (out / "solution_bad.go").write_text(bad)
    return ("ok", cid, f"pkg={pkg} tests={len(tests)} scaffold={len(scaffold)}")


def main() -> None:
    if not SRC.is_dir():
        raise SystemExit(f"clone aider first into {HERE / '_aider-src'}")
    if DST.exists():
        shutil.rmtree(DST)
    ok = skip = 0
    for d in sorted(SRC.iterdir()):
        if not d.is_dir() or not (d / ".meta" / "config.json").exists():
            continue
        if d.name in SKIP:
            print(f"  [skip] aider-{d.name}: {SKIP[d.name]}")
            skip += 1
            continue
        status, cid, msg = stage_one(d)
        print(f"  [{status}] {cid}: {msg}")
        ok += status == "ok"
        skip += status == "skip"
    print(f"\nstaged {ok}, skipped {skip} -> {DST}")


if __name__ == "__main__":
    main()
