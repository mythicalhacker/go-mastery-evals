#!/usr/bin/env python3
"""Go Mastery skill — eval harness CLI.

Examples:
    python run_evals.py --list
    python run_evals.py --selftest                       # grader sanity on fixtures
    python run_evals.py --validate-cases                 # every case has PASS/FAIL fixtures
    python run_evals.py --runner byo                     # grade outputs/ (any agent)
    python run_evals.py --runner anthropic --model claude-sonnet-4-6 --samples 3
    python run_evals.py --runner anthropic \\
        --models claude-haiku-4-5-20251001,claude-sonnet-4-6,claude-opus-4-8
    python run_evals.py --runner openai --model gpt-4.1 --only modern-errors-astype
    python run_evals.py --runner openai --model o4-mini      # reasoning model (param quirks handled)
    python run_evals.py --runner gemini --model gemini-2.5-pro   # Gemini via OpenAI-compat endpoint
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from harness.cases import load_cases  # noqa: E402
from harness.grader import go_env, grade, extract_code, toolchain_feedback  # noqa: E402
from harness.report import render, _safe  # noqa: E402
from harness import runners as R  # noqa: E402

WORKROOT = "/tmp"

# Reference fixtures every case must ship for --validate-cases / --selftest.
GOOD_FIXTURE = "solution_good.go"  # must grade PASS on its case
BAD_FIXTURE = "solution_bad.go"    # must grade FAIL on its case


def model_list(args):
    """Models to A/B in this invocation. --models wins; else --model; else [None]
    (the runner's default). BYO is model-agnostic but still gets one slot."""
    if args.models:
        return [m.strip() for m in args.models.split(",") if m.strip()]
    if args.model:
        return [args.model]
    return [None]


# Gemini speaks the OpenAI Chat Completions wire format at this endpoint, so the
# OpenAIRunner drives it with no extra dependency — just a preset base_url + key env.
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


def make_runner(args, model):
    if args.runner == "byo":
        return R.BYORunner(HERE / "outputs", HERE / "outputs" / "prompts")
    comp = getattr(args, "competitor_dir", None)
    if args.runner == "anthropic":
        return R.AnthropicRunner(model or "claude-sonnet-4-6", args.skill_dir, args.temperature, comp)
    if args.runner == "openai":
        return R.OpenAIRunner(model or "gpt-4.1", args.skill_dir, args.temperature, comp,
                              base_url=getattr(args, "base_url", None),
                              api_key_env=getattr(args, "api_key_env", "OPENAI_API_KEY"))
    if args.runner == "gemini":
        # Thin preset over OpenAIRunner; --base-url / --model still override.
        return R.OpenAIRunner(model or "gemini-2.5-pro", args.skill_dir, args.temperature, comp,
                              base_url=getattr(args, "base_url", None) or GEMINI_BASE_URL,
                              api_key_env="GEMINI_API_KEY")
    raise SystemExit(f"unknown runner: {args.runner}")


def model_id_of(runner, model_arg):
    """Stable id used to tag result rows / raw files / per-model reports."""
    return getattr(runner, "model", None) or model_arg or runner.name


def model_temps(runner_specs):
    """Per-model temperature *actually applied* (for honest per-model provenance).
    A model that rejected the param (e.g. claude-opus-4-8) reports that, not 0.0."""
    out = {}
    for runner, model_arg in runner_specs:
        mid = model_id_of(runner, model_arg)
        if not hasattr(runner, "temperature"):
            out[mid] = "n/a (model-agnostic runner)"
        elif getattr(runner, "_reject_temperature", False):
            out[mid] = "not applied — model rejected the parameter"
        else:
            out[mid] = runner.temperature
    return out


# --------------------------------------------------------------------------- #
# Fixture-based validation (shared by --validate-cases and --selftest)        #
# --------------------------------------------------------------------------- #

def _grade_fixture(case, fixture_name, expect_pass):
    """Grade one in-case fixture; return (ok, reason, case_result_or_None).

    ok  -> graded exactly as expected (pass when expect_pass, fail otherwise).
    """
    f = Path(case["_dir"]) / fixture_name
    if not f.exists():
        return None, f"missing {fixture_name}", None
    r = grade(case, f.read_text(), f"fixture:{fixture_name}", WORKROOT)
    return (r.passed == expect_pass), ("" if r.passed == expect_pass else
                                       f"graded passed={r.passed}, expected {expect_pass}"), r


def _failed_required(result):
    return [c for c in result.checks if c["required"] and not c["passed"]] if result else []


def _validate_cases(cases, *, require_fixtures, header):
    """Grade good (expect PASS) + bad (expect FAIL) fixtures for each case.

    require_fixtures=True  -> a missing fixture is a failure (--validate-cases).
    require_fixtures=False -> a missing fixture is skipped (--selftest: only
                              checks that the grader behaves where fixtures exist).
    Returns True if everything is green.
    """
    ok = True
    print(header + "\n")
    for case in cases:
        for fixture, expect in ((GOOD_FIXTURE, True), (BAD_FIXTURE, False)):
            good, reason, result = _grade_fixture(case, fixture, expect)
            if good is None:  # fixture absent
                if require_fixtures:
                    ok = False
                    print(f"  [XX] {case['id']}/{fixture}: {reason}")
                continue
            ok = ok and good
            mark = "OK" if good else "XX"
            tag = "good→PASS" if expect else "bad→FAIL"
            print(f"  [{mark}] {case['id']}/{fixture} ({tag}): {reason or 'ok'}")
            if not good:
                for c in _failed_required(result):
                    print(f"          - {c['name']}: {c['detail'][:120]}")
    return ok


def cmd_selftest(args):
    cases = load_cases(args.cases_dir, _only(args))
    ok = _validate_cases(
        cases, require_fixtures=False,
        header="Self-test — grader sanity on in-case good/bad fixtures:")
    print("\nSELFTEST:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


def cmd_validate_cases(args):
    cases = load_cases(args.cases_dir, _only(args))
    ok = _validate_cases(
        cases, require_fixtures=True,
        header="Validate-cases — every case must ship a PASS good + FAIL bad fixture:")
    print(f"\nVALIDATE-CASES ({len(cases)} cases):", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


# --------------------------------------------------------------------------- #
# Provenance                                                                  #
# --------------------------------------------------------------------------- #

def _go_version():
    try:
        p = subprocess.run(["go", "version"], capture_output=True, text=True,
                           env=go_env(), timeout=30)
        return p.stdout.strip() or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def _skill_fingerprint(skill_dir):
    """git SHA of the skill repo if available, else a content hash of its docs."""
    d = Path(skill_dir)
    if not d.exists():
        return "n/a (skill dir absent)"
    try:
        p = subprocess.run(["git", "-C", str(d), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=15)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout.strip() + " (git)"
    except Exception:  # noqa: BLE001
        pass
    h = hashlib.sha256()
    docs = sorted([d / "SKILL.md", *((d / "references").glob("*.md"))])
    for f in docs:
        if f.exists():
            h.update(f.read_bytes())
    return "sha256:" + h.hexdigest()[:12] + " (content)" if docs else "n/a"


def _provenance(args, runner_name, model_ids):
    """Shared provenance across all models in the run (per-model id injected later)."""
    return {
        "models": ", ".join(model_ids),
        "runner": runner_name,
        "temperature": args.temperature,
        "samples": args.samples,
        "fix_rounds": args.fix_rounds,
        "go_version": _go_version(),
        "skill_fingerprint": _skill_fingerprint(args.skill_dir),
        "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
    }


# --------------------------------------------------------------------------- #
# Main A/B loop                                                                #
# --------------------------------------------------------------------------- #

def _only(args):
    return set(args.only.split(",")) if args.only else None


_FIX_INSTRUCTION = (
    "Your previous Go code did not pass the toolchain. Fix EVERY issue listed below "
    "and return the corrected, COMPLETE program as EXACTLY ONE Go code block and "
    "nothing else.\n\nToolchain output:\n\n"
)


def _generate_self_correct(runner, case, variant, fix_rounds, workroot):
    """Agentic loop: generate, then let the model fix gofmt/build/vet/lint findings on
    its OWN code across up to ``fix_rounds`` rounds, exactly as it would in a real
    editor/CI. The hidden behavioral test is never surfaced (it stays the grading
    oracle), so this measures genuine self-correction, not answer leakage.

    Returns ``(final_text, src, rounds_used)``.
    """
    system = R.system_for(variant, runner.skill_dir, case, getattr(runner, "competitor_dir", None))
    messages = [{"role": "user", "content": case["prompt"]}]
    text = runner.chat(system, messages)
    used = 0
    for _ in range(fix_rounds):
        ok, feedback = toolchain_feedback(case, extract_code(text), None, workroot)
        if ok:
            break
        used += 1
        messages.append({"role": "assistant", "content": text})
        messages.append({"role": "user", "content": _FIX_INSTRUCTION + feedback})
        text = runner.chat(system, messages)
    return text, f"{runner.model}:{variant}+fix{used}", used


def main():
    ap = argparse.ArgumentParser(description="Go Mastery skill eval harness")
    ap.add_argument("--runner", default="byo", choices=["byo", "anthropic", "openai", "gemini"])
    ap.add_argument("--variants", default="with,without")
    ap.add_argument("--model", default=None, help="single model id (one of --models)")
    ap.add_argument("--models", default=None,
                    help="comma-separated model ids to A/B in one invocation")
    ap.add_argument("--base-url", dest="base_url", default=None,
                    help="OpenAI-compatible endpoint for --runner openai (e.g. a local "
                         "server or OpenRouter); --runner gemini presets the Google endpoint")
    ap.add_argument("--api-key-env", dest="api_key_env", default="OPENAI_API_KEY",
                    help="env var holding the API key for --runner openai (default OPENAI_API_KEY)")
    ap.add_argument("--temperature", type=float, default=0.0,
                    help="generation temperature (default 0.0 = deterministic)")
    ap.add_argument("--samples", type=int, default=1,
                    help="generations per (case, variant); report pass rate over them")
    ap.add_argument("--fix-rounds", dest="fix_rounds", type=int, default=0,
                    help="agentic self-correct: max rounds where the model is shown "
                         "gofmt/build/vet/lint output on its OWN code and fixes it "
                         "(the hidden behavioral test is never shown). 0 = off; try 2. "
                         "Requires an API runner.")
    ap.add_argument("--skill-dir", default=str(HERE.parent / "go-mastery"))
    ap.add_argument("--competitor-dir", dest="competitor_dir", default=None,
                    help="path to a competitor skill dir (SKILL.md [+ references/]) to "
                         "A/B against; enables the `competitor` variant. e.g. "
                         "--variants with,without,competitor --competitor-dir harness/competitors/jetbrains-go-modern")
    ap.add_argument("--cases-dir", default=str(HERE / "cases"))
    ap.add_argument("--only", default=None, help="comma-separated case ids")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validate-cases", dest="validate_cases", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return cmd_selftest(args)
    if args.validate_cases:
        return cmd_validate_cases(args)

    cases = load_cases(args.cases_dir, _only(args))

    if args.list:
        for c in cases:
            print(f"{c['id']:34s} {c.get('category', ''):16s} {c.get('title', '')}")
        print(f"\n{len(cases)} cases")
        return

    variants = [v.strip() for v in args.variants.split(",") if v.strip()]
    samples = max(1, args.samples)
    if samples > 1 and args.temperature == 0:
        print("[note] temp 0 is not fully deterministic on the API; sampling "
              "stabilizes per-case verdicts via majority vote.")
    raw_dir = HERE / "results" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    runner_specs = [(make_runner(args, m), m) for m in model_list(args)]
    results, pending = [], 0

    try:
        for runner, model_arg in runner_specs:
            model_id = model_id_of(runner, model_arg)
            for c in cases:
                for v in variants:
                    for s in range(samples):
                        # Isolate every generation: one model/case error must not
                        # abort the whole multi-tier run.
                        try:
                            if args.fix_rounds > 0 and hasattr(runner, "chat"):
                                out, src, fixn = _generate_self_correct(
                                    runner, c, v, args.fix_rounds, WORKROOT)
                            else:
                                out, src = runner.generate(c, v)
                                fixn = 0
                        except Exception as e:  # noqa: BLE001
                            results.append({
                                "case_id": c["id"], "variant": v, "passed": False,
                                "checks": [], "code_len": 0, "sample": s,
                                "source": "error", "model": model_id,
                                "error": str(e)[:500],
                            })
                            print(f"[error] {model_id} · {c['id']} [{v}]: "
                                  f"{str(e).splitlines()[0][:160]}")
                            continue
                        if out is None:  # BYO with no output yet — prompt was written
                            pending += 1
                            print(f"[pending] {c['id']} [{v}] -> prompt written to outputs/prompts/")
                            break  # re-generating won't change anything; skip remaining samples
                        # Persist raw generation (tagged by model) so failures are debuggable.
                        (raw_dir / f"{_safe(model_id)}__{c['id']}__{v}__s{s}.txt").write_text(out)
                        r = grade(c, out, v, WORKROOT)
                        d = r.to_dict()
                        d["sample"] = s
                        d["source"] = src
                        d["model"] = model_id
                        d["fix_rounds_used"] = fixn
                        results.append(d)
                        tag = f" {s + 1}/{samples}" if samples > 1 else ""
                        print(f"[{'PASS' if r.passed else 'FAIL'}] {model_id} · {c['id']} [{v}]{tag} ({src})")
    finally:
        # Always emit the report on whatever was collected, even on partial failure.
        if results:
            prov = _provenance(args, args.runner,
                               list(dict.fromkeys(r["model"] for r in results)))
            rep = render(results, cases, HERE / "results", provenance=prov,
                         model_meta=model_temps(runner_specs), raw_dir=raw_dir)
            print(f"\nReport: {rep}")
        if pending:
            print(f"\n{pending} pending — fill outputs/ (see outputs/prompts/) then re-run.")


if __name__ == "__main__":
    main()
