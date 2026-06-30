"""Generation runners — how a (case, variant) becomes model output to grade.

Two families:
  * BYORunner       — model-agnostic. Reads pre-generated outputs from outputs/,
                      or writes the exact prompt for you to run in any agent.
  * AnthropicRunner / OpenAIRunner — automated A/B via API (needs an API key).

The "with" variant injects the skill (SKILL.md + any case-named references,
mirroring INDEX routing) as system context; "without" uses only a neutral
instruction. Everything else is held constant so the delta isolates the skill.
"""
from __future__ import annotations

import os
from pathlib import Path

NEUTRAL_SYS = (
    "You are an expert Go engineer. Implement the user's request as production-grade, "
    "idiomatic Go. Output EXACTLY ONE Go code block and nothing else — no prose, no "
    "alternatives, no commentary."
)


def build_skill_context(skill_dir, refs):
    parts = []
    skill_md = Path(skill_dir) / "SKILL.md"
    if skill_md.exists():
        parts.append(skill_md.read_text())
    for r in refs or []:
        p = Path(skill_dir) / "references" / r
        if p.exists():
            parts.append(f"\n\n# reference: {r}\n" + p.read_text())
    return "\n\n".join(parts)


def system_for(variant, skill_dir, case, competitor_dir=None):
    """System prompt for a variant.

    with        -> our skill (SKILL.md + the case's named references)
    competitor  -> a competitor skill from competitor_dir, injected the same way
                   (its SKILL.md + any references/ that match the case's skill_refs).
                   A single-file competitor (e.g. JetBrains go-modern-guidelines) just
                   contributes its SKILL.md; a multi-skill competitor can be staged into
                   competitor_dir with our reference names for per-case routing.
    without     -> neutral prompt only (baseline)
    """
    if variant == "with":
        ctx = build_skill_context(skill_dir, case.get("skill_refs"))
        return ctx + "\n\n---\n\n" + NEUTRAL_SYS
    if variant == "competitor" and competitor_dir:
        ctx = build_skill_context(competitor_dir, case.get("skill_refs"))
        return (ctx + "\n\n---\n\n" + NEUTRAL_SYS) if ctx else NEUTRAL_SYS
    return NEUTRAL_SYS


class BYORunner:
    """Bring-your-own-output: grade outputs you produced with any agent."""

    name = "byo"

    def __init__(self, outputs_dir, prompts_dir):
        self.out = Path(outputs_dir)
        self.prompts = Path(prompts_dir)

    def generate(self, case, variant, **_):
        for ext in ("go", "txt", "md"):
            f = self.out / f"{case['id']}__{variant}.{ext}"
            if f.exists():
                return f.read_text(), f"byo:{f.name}"
        # No output yet: emit the prompt for the user to run, mark pending.
        self.prompts.mkdir(parents=True, exist_ok=True)
        note = "INJECT skill (SKILL.md as system prompt)" if variant == "with" else "NO skill"
        (self.prompts / f"{case['id']}__{variant}.md").write_text(
            f"# {case['id']}  ·  variant: {variant}  ·  {note}\n\n"
            f"Run this prompt, then save the model's reply to "
            f"`outputs/{case['id']}__{variant}.go` (or .txt/.md).\n\n"
            f"## Prompt\n\n{case['prompt']}\n"
        )
        return None, "pending"


class AnthropicRunner:
    """Automated A/B against the Anthropic API (reads ANTHROPIC_API_KEY)."""

    name = "anthropic"

    def __init__(self, model, skill_dir, temperature=0.0, competitor_dir=None):
        try:
            import anthropic  # lazy import so BYO mode needs no SDK
        except ImportError:
            raise SystemExit(
                "The 'anthropic' SDK is required for --runner anthropic.\n"
                "  install:  pip install anthropic   (or: pip install -r requirements-api.txt)\n"
                "  then set: export ANTHROPIC_API_KEY=sk-..."
            )
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise SystemExit(
                "ANTHROPIC_API_KEY is not set.\n"
                "  run:  export ANTHROPIC_API_KEY=sk-...   then retry."
            )
        self.client = anthropic.Anthropic()
        self.model = model
        self.skill_dir = skill_dir
        self.competitor_dir = competitor_dir
        self.temperature = temperature
        # Some models (e.g. claude-opus-4-8) reject the temperature param ("temperature
        # is deprecated for this model"). Detected once, then skipped for this run.
        self._bad_request = getattr(anthropic, "BadRequestError", Exception)
        self._reject_temperature = False

    def chat(self, system, messages):
        """One completion given a full system prompt + message history (multi-turn).

        The agentic self-correct loop calls this repeatedly, appending the model's
        prior reply and a toolchain-feedback user turn.
        """
        kwargs = dict(
            model=self.model,
            max_tokens=4096,  # skill responses run longer; don't truncate the final block
            system=system,
            messages=messages,
        )
        if self.temperature is not None and not self._reject_temperature:
            kwargs["temperature"] = self.temperature
        try:
            msg = self.client.messages.create(**kwargs)
        except self._bad_request as e:
            # Retry once without temperature if that's what the model objected to.
            if "temperature" in kwargs and "temperature" in str(e).lower():
                self._reject_temperature = True
                kwargs.pop("temperature", None)
                msg = self.client.messages.create(**kwargs)
            else:
                raise
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")

    def generate(self, case, variant, **_):
        system = system_for(variant, self.skill_dir, case, getattr(self, "competitor_dir", None))
        text = self.chat(system, [{"role": "user", "content": case["prompt"]}])
        return text, f"{self.model}:{variant}"


class OpenAIRunner:
    """Automated A/B against any OpenAI-compatible Chat Completions API.

    Defaults to OpenAI (OPENAI_API_KEY). With ``base_url`` + ``api_key_env`` the SAME
    runner drives Google Gemini (its OpenAI-compatible endpoint), OpenRouter, or a
    local server — no extra dependency, since they all speak the Chat Completions
    wire format. The skill is a system-prompt injection and grading is on the emitted
    Go, so the A/B is identical across vendors; only this runner changes.
    """

    name = "openai"

    # 4096 is fine for chat models. But on REASONING models the hidden reasoning
    # tokens count against the completion-token budget, so a small cap returns
    # empty/truncated content — the case would fail for the wrong reason. Give the
    # completion-tokens path real headroom.
    _CHAT_MAX_TOKENS = 4096
    _REASONING_MAX_TOKENS = 16384

    def __init__(self, model, skill_dir, temperature=0.0, competitor_dir=None,
                 base_url=None, api_key_env="OPENAI_API_KEY"):
        try:
            import openai  # lazy import so BYO/anthropic modes need no SDK
            from openai import OpenAI
        except ImportError:
            raise SystemExit(
                "The 'openai' SDK is required for --runner openai/gemini.\n"
                "  install:  pip install openai   (or: pip install -r requirements-api.txt)\n"
                f"  then set: export {api_key_env}=..."
            )
        key = os.environ.get(api_key_env)
        if not key:
            raise SystemExit(
                f"{api_key_env} is not set.\n"
                f"  run:  export {api_key_env}=...   then retry."
            )
        self.client = OpenAI(base_url=base_url or None, api_key=key)
        self.model = model
        self.skill_dir = skill_dir
        self.competitor_dir = competitor_dir
        self.temperature = temperature
        # Param-quirk guards, detected-once-and-cached (mirrors AnthropicRunner):
        #  * some models reject `max_tokens` and require `max_completion_tokens` (gpt-5.x);
        #  * reasoning models (o-series, gpt-5-class) reject a non-default `temperature`.
        # A model can reject one on the first call and the other on the next, so chat()
        # learns BOTH across retries — stripping/swapping only the param the error names.
        self._bad_request = getattr(openai, "BadRequestError", Exception)
        self._reject_temperature = False
        self._use_completion_tokens = False

    def _token_kwargs(self):
        if self._use_completion_tokens:
            return {"max_completion_tokens": self._REASONING_MAX_TOKENS}
        return {"max_tokens": self._CHAT_MAX_TOKENS}

    def chat(self, system, messages):
        """One completion (multi-turn). Learns and caches per-model param quirks across
        retries, swapping only the exact param the BadRequestError names — any other
        error propagates unchanged (never silently swallowed)."""
        full = [{"role": "system", "content": system}] + messages
        while True:
            kwargs = dict(model=self.model, messages=full, **self._token_kwargs())
            if self.temperature is not None and not self._reject_temperature:
                kwargs["temperature"] = self.temperature
            try:
                r = self.client.chat.completions.create(**kwargs)
                return r.choices[0].message.content
            except self._bad_request as e:
                msg = str(e).lower()
                # Swap to max_completion_tokens ONLY when the error explicitly says so
                # (so a "max_tokens too large" value error isn't mis-handled).
                if "max_tokens" in kwargs and "max_completion_tokens" in msg:
                    self._use_completion_tokens = True
                    continue
                if "temperature" in kwargs and "temperature" in msg:
                    self._reject_temperature = True
                    continue
                raise

    def generate(self, case, variant, **_):
        system = system_for(variant, self.skill_dir, case, getattr(self, "competitor_dir", None))
        text = self.chat(system, [{"role": "user", "content": case["prompt"]}])
        return text, f"{self.model}:{variant}"
