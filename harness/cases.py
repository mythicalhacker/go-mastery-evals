"""Discover and load eval cases (one directory per case).

Layout:
    cases/<id>/
        case.yaml     # metadata + grading rules
        prompt.md     # the task given to the model
        test.go       # optional behavioral test (package solution)
        files/        # optional extra scaffold files copied into the module
"""
from __future__ import annotations

from pathlib import Path

import yaml


def load_cases(cases_dir, only=None):
    cases = []
    for d in sorted(Path(cases_dir).iterdir()):
        if not d.is_dir():
            continue
        meta = d / "case.yaml"
        if not meta.exists():
            continue
        case = yaml.safe_load(meta.read_text()) or {}
        case["_dir"] = str(d)
        case.setdefault("id", d.name)
        prompt = d / "prompt.md"
        case["prompt"] = prompt.read_text().strip() if prompt.exists() else case.get("prompt", "")
        if only and case["id"] not in only:
            continue
        cases.append(case)
    return cases
