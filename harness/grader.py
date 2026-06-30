"""Toolchain-based grader.

The Go toolchain *is* the grader: generated code is assembled into a temporary
module and checked with gofmt / go vet / go build / go test (+ optional
golangci-lint and -race), plus regex idiom checks (must_match / must_not_match).

This module has no model dependencies — it grades a string of Go source,
however that string was produced.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field, asdict
from pathlib import Path

_FENCE_RE = re.compile(r"```(?:go|golang)?\s*\n(.*?)```", re.DOTALL)

# A pre-vendored template module (go.mod + go.sum + vendor/) lets candidates that
# use the allowed golang.org/x/* packages (errgroup, semaphore, rate, exp) build
# OFFLINE via -mod=vendor, while arbitrary third-party imports still fail. Built
# once with `make vendor`; absent it, the grader falls back to a bare stdlib-only
# module (GOPROXY=off, -mod=mod) so existing cases keep working.
_HARNESS_DIR = Path(__file__).resolve().parent


def _vendored_template(name: str = "_gomod_template"):
    """Return a pre-vendored template module dir by name, or None if not vendored.

    Default is the lean stdlib + golang.org/x/* template. A case may set
    ``module_template: ext`` in case.yaml to build against ``_gomod_template_ext``
    (grpc, etc.), so niche behavioral cases compile offline without bloating or
    slowing the stdlib-only cases.
    """
    t = _HARNESS_DIR / name
    return t if (t / "vendor" / "modules.txt").exists() else None


def _template_for(case: dict):
    name = "_gomod_template_ext" if case.get("module_template") == "ext" else "_gomod_template"
    return _vendored_template(name)


def _stage(case, code, work, env):
    """Write a buildable module (vendored template or bare go.mod + the candidate
    file, package-normalized) into ``work``; return the env to use (GOFLAGS set to
    -mod=vendor when a template is staged). Shared by the deterministic quality
    dimensions so they build a candidate exactly the way ``grade`` does.
    """
    template = _template_for(case)
    if template is not None:
        shutil.copytree(template, work, dirs_exist_ok=True)
        env = dict(env)
        env["GOFLAGS"] = "-mod=vendor"
    else:
        (work / "go.mod").write_text(
            f"module evalcase\n\ngo {case.get('go_version', '1.26')}\n")
    (work / case.get("filename", "solution.go")).write_text(
        _normalize_package(code, case.get("package", "solution")))
    return env


def extract_code(text: str) -> str:
    """Pull Go source out of a model response, stripping prose and markdown fences.

    Takes the LAST fenced block containing a `package` declaration. Models that
    self-correct emit a buggy block and then a fixed one (this gets more common
    with the skill, which makes responses chattier); the final block is the
    answer, so picking by recency — not by size — avoids grading a draft the
    model already discarded. Falls back to the last fenced block, then raw text.
    """
    if not text:
        return ""
    blocks = _FENCE_RE.findall(text)
    if blocks:
        with_pkg = [b for b in blocks if re.search(r"^\s*package\s+\w+", b, re.M)]
        candidates = with_pkg or blocks
        return candidates[-1].strip() + "\n"
    return text.strip() + "\n"


_PKG_RE = re.compile(r"^[ \t]*package[ \t]+\w+", re.M)


def _normalize_package(code: str, pkg: str) -> str:
    """Rewrite the candidate's first ``package`` clause to the expected name.

    The harness fixes the filename and the test file's package, so the candidate's
    package *name* is arbitrary scaffolding. A model that wrote ``package main``
    (common for cgo) or ``package stats`` would otherwise collide with the
    ``package solution`` test file ("found packages main and solution") and fail on
    a build-setup error instead of being graded on its actual logic. Normalizing is
    boilerplate hygiene, like renaming test.go -> *_test.go.
    """
    return _PKG_RE.sub(f"package {pkg}", code, count=1)


def strip_comments(src: str) -> str:
    """Remove Go line (``//``) and block (``/* */``) comments from *src*.

    Interpreted strings ``"..."``, raw strings ``` `...` ```, and rune literals
    ``'...'`` are preserved verbatim (honoring backslash escapes), because idiom
    tokens such as ``$1`` or ``%w`` legitimately live inside string literals — we
    strip comments *only*, never strings. Newlines are kept so line numbers stay
    stable; other comment characters are dropped.

    A small char-by-char state machine; ``//`` inside a string (e.g. the
    ``http://`` in a URL) is therefore not treated as a comment.
    """
    out = []
    i, n = 0, len(src)
    state = "code"  # code | line | block | string | raw | rune
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if state == "code":
            if c == "/" and nxt == "/":
                state, i = "line", i + 2
            elif c == "/" and nxt == "*":
                state, i = "block", i + 2
            else:
                if c == '"':
                    state = "string"
                elif c == "`":
                    state = "raw"
                elif c == "'":
                    state = "rune"
                out.append(c)
                i += 1
        elif state == "line":
            if c == "\n":
                state = "code"
                out.append(c)  # keep the newline that ends the comment
            i += 1
        elif state == "block":
            if c == "*" and nxt == "/":
                state, i = "code", i + 2
            else:
                if c == "\n":
                    out.append(c)  # preserve internal newlines (line stability)
                i += 1
        elif state in ("string", "rune"):
            out.append(c)
            if c == "\\":  # escape: emit the escaped char too, don't end literal
                if i + 1 < n:
                    out.append(src[i + 1])
                i += 2
                continue
            if (state == "string" and c == '"') or (state == "rune" and c == "'"):
                state = "code"
            i += 1
        elif state == "raw":
            out.append(c)
            if c == "`":  # raw strings have no escapes
                state = "code"
            i += 1
    return "".join(out)


def _run(cmd, cwd, env, timeout=120):
    try:
        p = subprocess.run(
            cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",  # some tests print raw/invalid bytes
        )
        return p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        return 124, f"timeout after {timeout}s"
    except FileNotFoundError as e:
        return 127, f"command not found: {e}"


def go_env(base=None):
    """Build an environment for invoking the Go toolchain.

    Honors an explicit GOROOT (used in the sandbox) and ensures writable cache
    dirs. On a normal dev machine where `go` is on PATH, the defaults are fine.

    Determinism guards (forced, not just defaulted): cases are stdlib-only by
    contract, so we hard-disable the module proxy, the checksum database, and
    toolchain auto-download. Any accidental third-party import or network
    dependency then fails fast with a clear build error instead of silently
    reaching out — keeping every grade reproducible and offline.
    """
    env = dict(os.environ if base is None else base)
    env.setdefault("GOCACHE", os.path.join(tempfile.gettempdir(), "gocache"))
    env.setdefault("GOPATH", os.path.join(tempfile.gettempdir(), "gopath"))
    env.setdefault("GOFLAGS", "-mod=mod")
    env["GOTOOLCHAIN"] = "local"  # never download a toolchain
    env["GOPROXY"] = "off"        # never fetch modules: stdlib-only, offline
    env["GOSUMDB"] = "off"        # no checksum-db network calls
    if env.get("GOROOT"):
        env["PATH"] = os.path.join(env["GOROOT"], "bin") + os.pathsep + env.get("PATH", "")
    return env


def _apply_target(env, case):
    """Apply a case's cross-build target (GOOS/GOARCH) when set — e.g. an ebpf case
    (linux-only) or a wasm case (wasip1/js) must cross-compile so it builds on any
    host (incl. macOS). Forces CGO off for a clean cross-compile. Such cases are
    build/vet-only (the artifact can't run on the host), so they must not set
    ``test: true``.
    """
    if case.get("goos"):
        env = dict(env)
        env["GOOS"] = case["goos"]
        if case.get("goarch"):
            env["GOARCH"] = case["goarch"]
        env["CGO_ENABLED"] = "0"
    return env


def _have(tool, env):
    return shutil.which(tool, path=env.get("PATH")) is not None


_ISSUE_LINE = re.compile(r"^\S.*:\d+:\d+:\s")  # golangci-lint "file:line:col: msg" finding


def _golangci_issues(work, env):
    """Run golangci-lint in an already-staged module; return ``(issues, detail)``.

    ``issues`` is an int count (0 = clean) so quality can subtract a per-issue
    weight; it is ``None`` when the dimension can't be measured — tool absent, or a
    tooling/version error — so a golangci-lint hiccup degrades to a skip instead of
    masquerading as a code failure. Version-proof: parses the default text output
    (no format flags), counting ``file:line:col:`` finding lines.
    """
    if not _have("golangci-lint", env):
        return None, "golangci-lint not installed"
    rc, out = _run(["golangci-lint", "run", "--tests=false", "./..."], work, env, timeout=180)
    if rc not in (0, 1):  # 0 clean, 1 findings; anything else = tooling/config/version error
        return None, f"golangci-lint tooling error rc={rc}: {out[:200]}"
    if rc == 0:
        return 0, "clean"
    n = sum(1 for ln in out.splitlines() if _ISSUE_LINE.match(ln))
    return (n or 1), out[:400]  # rc=1 with no parseable finding lines still means ≥1


@dataclass
class CheckResult:
    name: str
    passed: bool
    required: bool
    detail: str = ""


@dataclass
class CaseResult:
    case_id: str
    variant: str
    passed: bool
    checks: list = field(default_factory=list)
    code_len: int = 0

    def to_dict(self):
        return asdict(self)


def grade(case: dict, code_text: str, variant: str, workroot: str, env=None) -> CaseResult:
    """Grade one (case, variant) given the model's raw output `code_text`."""
    env = _apply_target(go_env(env), case)
    cfg = case.get("checks", {})
    code = _normalize_package(extract_code(code_text), case.get("package", "solution"))
    res = CaseResult(case_id=case["id"], variant=variant, passed=False, code_len=len(code))
    results: list[CheckResult] = []

    def add(name, passed, required, detail=""):
        results.append(CheckResult(name, passed, required, (detail or "")[:1500]))

    work = Path(tempfile.mkdtemp(prefix=f"eval_{case['id']}_{variant}_", dir=workroot))
    try:
        template = _template_for(case)
        if template is not None:
            # Build inside a copy of the vendored template: stdlib + the allowed
            # golang.org/x/* resolve offline from vendor/; anything else fails.
            shutil.copytree(template, work, dirs_exist_ok=True)
            env["GOFLAGS"] = "-mod=vendor"
        else:
            (work / "go.mod").write_text(
                f"module evalcase\n\ngo {case.get('go_version', '1.26')}\n")
        (work / case.get("filename", "solution.go")).write_text(code)

        casedir = Path(case["_dir"])
        test_present = (casedir / "test.go").exists()
        if cfg.get("test") and test_present:
            shutil.copy(casedir / "test.go", work / "solution_test.go")
        files_dir = casedir / "files"
        if files_dir.is_dir():
            for f in files_dir.iterdir():
                if f.is_file():
                    shutil.copy(f, work / f.name)

        if cfg.get("gofmt"):
            solfile = case.get("filename", "solution.go")
            rc, out = _run(["gofmt", "-l", solfile], work, env)
            # gofmt -l lists files needing formatting; we grade only the model's file
            add("gofmt", rc == 0 and out.strip() == "", True, out or f"rc={rc}")
        if cfg.get("vet"):
            rc, out = _run(["go", "vet", "./..."], work, env)
            add("vet", rc == 0, True, out)
        if cfg.get("build", True):
            rc, out = _run(["go", "build", "./..."], work, env)
            add("build", rc == 0, True, out)
        if cfg.get("test"):
            if not test_present:
                add("test", False, True, "checks.test set but no test.go in case dir")
            else:
                # -timeout makes a blocking/deadlocked candidate fail fast (panic:
                # test timed out) instead of hanging the whole suite — a correct FAIL.
                cmd = ["go", "test", "-timeout", "30s", "./..."]
                if cfg.get("race"):
                    cmd.insert(2, "-race")
                rc, out = _run(cmd, work, env, timeout=180)
                add("test", rc == 0, True, out)
        if cfg.get("lint", True):  # default ON — the toughened bar (staticcheck/ineffassign/unused/…)
            issues, detail = _golangci_issues(work, env)
            if issues is None:  # tool absent or tooling error → non-required skip, never a false fail
                add("lint", True, False, f"golangci-lint skipped: {detail} — install it for the full gate")
            else:  # int count surfaced in detail so quality can reuse it; 0 = required-pass
                add("lint", issues == 0, True, "0 issues (clean)" if issues == 0 else f"{issues} issue(s)\n{detail}")

        # Idiom regexes match against comment-stripped source so a mention of an
        # idiom in a comment can't create false signal (string literals are kept).
        match_src = strip_comments(code)
        for pat in cfg.get("must_match", []):
            ok = re.search(pat, match_src) is not None
            add(f"must_match:{pat}", ok, True, "" if ok else "pattern not found")
        for pat in cfg.get("must_not_match", []):
            ok = re.search(pat, match_src) is None
            add(f"must_not_match:{pat}", ok, True, "" if ok else "forbidden pattern present")

        res.checks = [asdict(c) for c in results]
        required = [c for c in results if c.required]
        res.passed = bool(required) and all(c.passed for c in required)
        return res
    finally:
        shutil.rmtree(work, ignore_errors=True)


def toolchain_feedback(case: dict, code: str, env=None, workroot=".") -> tuple[bool, str]:
    """Run formatter/compiler/vet/lint on the candidate's OWN code and return
    ``(ok, feedback)`` for the agentic self-correct loop.

    Deliberately excludes the behavioral test (``test.go``): that file is the
    grading oracle and must never be shown to the model, or the eval would leak
    its own answer. This gives exactly the signals a developer/agent sees by
    running ``gofmt``/``go build``/``go vet``/``golangci-lint`` on their code —
    the mechanical layer — while logic correctness stays judged by the held-out
    test at final grading time.
    """
    env = _apply_target(go_env(env), case)
    work = Path(tempfile.mkdtemp(prefix=f"fix_{case['id']}_", dir=workroot))
    try:
        template = _template_for(case)
        if template is not None:
            shutil.copytree(template, work, dirs_exist_ok=True)
            env["GOFLAGS"] = "-mod=vendor"
        else:
            (work / "go.mod").write_text(
                f"module evalcase\n\ngo {case.get('go_version', '1.26')}\n")
        sol = case.get("filename", "solution.go")
        (work / sol).write_text(_normalize_package(code, case.get("package", "solution")))

        msgs = []
        rc, out = _run(["gofmt", "-l", sol], work, env)
        if rc != 0 or out.strip():
            _, diff = _run(["gofmt", "-d", sol], work, env)
            msgs.append("gofmt: file is not formatted (run gofmt). Diff:\n" + (diff or out))
        rc, out = _run(["go", "build", "./..."], work, env)
        if rc != 0:
            msgs.append("go build failed:\n" + out)
        rc, out = _run(["go", "vet", "./..."], work, env)
        if rc != 0:
            msgs.append("go vet failed:\n" + out)
        issues, detail = _golangci_issues(work, env)
        if issues:  # only surface real findings (None = skip, 0 = clean)
            msgs.append("golangci-lint findings:\n" + detail)
        return (not msgs), "\n\n".join(msgs)[:4000]
    finally:
        shutil.rmtree(work, ignore_errors=True)


def gofmt_clean(case, code, env=None, workroot="/tmp"):
    """Deterministic quality dimension: is the candidate gofmt-clean (boolean)?
    ``None`` if the Go toolchain is unavailable — the dimension is then skipped
    (graceful degradation, like the ``skipUnless`` tests)."""
    case = case or {}
    env = _apply_target(go_env(env), case)
    if not _have("gofmt", env):
        return None
    work = Path(tempfile.mkdtemp(prefix=f"qfmt_{case.get('id', 'x')}_", dir=workroot))
    try:
        env = _stage(case, code, work, env)
        rc, out = _run(["gofmt", "-l", case.get("filename", "solution.go")], work, env)
        return rc == 0 and out.strip() == ""
    finally:
        shutil.rmtree(work, ignore_errors=True)


def lint_issues(case, code, env=None, workroot="/tmp"):
    """Deterministic quality dimension: golangci-lint issue count for the candidate
    (int, 0 = clean). ``None`` if Go or golangci-lint is unavailable (skipped)."""
    case = case or {}
    env = _apply_target(go_env(env), case)
    if not _have("go", env):
        return None
    work = Path(tempfile.mkdtemp(prefix=f"qlint_{case.get('id', 'x')}_", dir=workroot))
    try:
        env = _stage(case, code, work, env)
        return _golangci_issues(work, env)[0]
    finally:
        shutil.rmtree(work, ignore_errors=True)
