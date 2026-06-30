"""Unit tests for the runner layer (Anthropic temperature guard; OpenAI-compatible
runner param quirks + base_url/key wiring for OpenAI & Gemini).

No network and no SDK construction: __init__ is bypassed (or a fake ``openai``
module is injected), so these run anywhere with no keys.

Run:  python -m unittest discover -s tests
"""
import os
import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness import runners as R  # noqa: E402


class _FakeMsg:
    def __init__(self, text):
        block = type("B", (), {"type": "text", "text": text})()
        self.content = [block]


class _FakeMessages:
    """Records every create() call; optionally rejects the temperature kwarg."""

    def __init__(self, reject_temp):
        self.reject_temp = reject_temp
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(dict(kwargs))
        if self.reject_temp and "temperature" in kwargs:
            raise RuntimeError("400 temperature is deprecated for this model")
        return _FakeMsg("package solution\n")


class _FakeClient:
    def __init__(self, reject_temp):
        self.messages = _FakeMessages(reject_temp)


def _runner(reject_temp, temperature=0.0):
    r = R.AnthropicRunner.__new__(R.AnthropicRunner)  # bypass __init__ (no SDK/key)
    r.model = "fake-model"
    r.skill_dir = "/nonexistent-skill-dir"  # never read: "without" uses the neutral prompt
    r.temperature = temperature
    r._bad_request = RuntimeError  # treat the fake's error as the "bad request" type
    r._reject_temperature = False
    r.client = _FakeClient(reject_temp)
    return r


CASE = {"id": "x", "prompt": "do a thing"}


class TemperatureResilienceTest(unittest.TestCase):
    def test_rejecting_model_retries_without_temperature_then_caches(self):
        r = _runner(reject_temp=True)
        text, _ = r.generate(CASE, "without")
        self.assertIn("package solution", text)
        calls = r.client.messages.calls
        self.assertEqual(len(calls), 2)               # first try + retry
        self.assertIn("temperature", calls[0])        # first attempt sends it
        self.assertNotIn("temperature", calls[1])     # retry drops it
        self.assertTrue(r._reject_temperature)        # cached for the run
        r.generate(CASE, "without")                   # next call skips it entirely
        self.assertEqual(len(r.client.messages.calls), 3)
        self.assertNotIn("temperature", r.client.messages.calls[2])

    def test_accepting_model_keeps_temperature(self):
        r = _runner(reject_temp=False)
        r.generate(CASE, "without")
        calls = r.client.messages.calls
        self.assertEqual(len(calls), 1)
        self.assertIn("temperature", calls[0])
        self.assertFalse(r._reject_temperature)

    def test_temperature_none_is_omitted(self):
        r = _runner(reject_temp=False, temperature=None)
        r.generate(CASE, "without")
        self.assertNotIn("temperature", r.client.messages.calls[0])

    def test_non_temperature_bad_request_propagates(self):
        # A 400 that is not about temperature must not be silently swallowed.
        r = _runner(reject_temp=False)

        def boom(**kwargs):
            raise RuntimeError("400 max_tokens too large")

        r.client.messages.create = boom
        with self.assertRaises(RuntimeError):
            r.generate(CASE, "without")


# --------------------------------------------------------------------------- #
# OpenAI-compatible runner: param-quirk guard (offline; fake nested client)    #
# --------------------------------------------------------------------------- #

class _FakeBadReq(Exception):
    """Stands in for openai.BadRequestError."""


class _FakeCompletions:
    """Records create() calls; rejects named params with the real-world 400 messages."""

    def __init__(self, reject):
        self.reject = set(reject)
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(dict(kwargs))
        if "max_tokens" in self.reject and "max_tokens" in kwargs:
            raise _FakeBadReq("400 Unsupported parameter: 'max_tokens' is not supported "
                              "with this model. Use 'max_completion_tokens' instead.")
        if "temperature" in self.reject and "temperature" in kwargs:
            raise _FakeBadReq("400 Unsupported value: 'temperature' does not support 0.0 "
                              "with this model. Only the default (1) value is supported.")
        msg = type("M", (), {"content": "package solution\n"})()
        return type("R", (), {"choices": [type("C", (), {"message": msg})()]})()


class _FakeOAIClient:
    def __init__(self, reject):
        self.completions = _FakeCompletions(reject)
        self.chat = type("Chat", (), {"completions": self.completions})()


def _oai_runner(reject=(), temperature=0.0):
    r = R.OpenAIRunner.__new__(R.OpenAIRunner)  # bypass __init__ (no SDK/key)
    r.model, r.skill_dir, r.competitor_dir = "fake", "/nonexistent", None
    r.temperature = temperature
    r._bad_request = _FakeBadReq
    r._reject_temperature = False
    r._use_completion_tokens = False
    r.client = _FakeOAIClient(reject)
    return r


_MSG = [{"role": "user", "content": "hi"}]


class OpenAIParamQuirkTest(unittest.TestCase):
    def test_temperature_rejected_retried_and_cached(self):
        r = _oai_runner(reject={"temperature"})
        self.assertIn("package solution", r.chat("sys", _MSG))
        calls = r.client.completions.calls
        self.assertEqual(len(calls), 2)
        self.assertIn("temperature", calls[0])
        self.assertNotIn("temperature", calls[1])
        self.assertTrue(r._reject_temperature)
        r.chat("sys", _MSG)  # cached: temperature never sent again
        self.assertNotIn("temperature", r.client.completions.calls[2])

    def test_max_tokens_swapped_to_completion_tokens_with_headroom(self):
        r = _oai_runner(reject={"max_tokens"})
        self.assertIn("package solution", r.chat("sys", _MSG))
        calls = r.client.completions.calls
        self.assertEqual(len(calls), 2)
        self.assertIn("max_tokens", calls[0])
        self.assertNotIn("max_tokens", calls[1])
        self.assertIn("max_completion_tokens", calls[1])
        # reasoning-token headroom: a small cap would truncate the answer
        self.assertGreaterEqual(calls[1]["max_completion_tokens"], 16384)
        self.assertTrue(r._use_completion_tokens)

    def test_both_quirks_learned_across_retries(self):
        # Reject max_tokens on call 1, temperature on call 2; call 3 succeeds.
        r = _oai_runner(reject={"max_tokens", "temperature"})
        self.assertIn("package solution", r.chat("sys", _MSG))
        calls = r.client.completions.calls
        self.assertEqual(len(calls), 3)
        self.assertNotIn("max_tokens", calls[2])
        self.assertNotIn("temperature", calls[2])
        self.assertIn("max_completion_tokens", calls[2])
        self.assertTrue(r._use_completion_tokens and r._reject_temperature)

    def test_unrelated_bad_request_propagates(self):
        r = _oai_runner(reject=())

        def boom(**kwargs):
            raise _FakeBadReq("400 context_length_exceeded")

        r.client.completions.create = boom
        with self.assertRaises(_FakeBadReq):
            r.chat("sys", _MSG)


# --------------------------------------------------------------------------- #
# Client construction wiring: base_url + api_key_env (OpenAI & Gemini preset)  #
# --------------------------------------------------------------------------- #

class _ClientWiringTest(unittest.TestCase):
    """Inject a fake ``openai`` module so __init__/make_runner construct offline and we
    can capture the OpenAI(...) constructor kwargs."""

    def _install_fake_openai(self):
        captured = {}

        class FakeBadRequest(Exception):
            pass

        class FakeClient:
            def __init__(self, **kwargs):
                captured["kwargs"] = kwargs

        mod = types.ModuleType("openai")
        mod.OpenAI = FakeClient
        mod.BadRequestError = FakeBadRequest
        old = sys.modules.get("openai")
        sys.modules["openai"] = mod
        self.addCleanup(lambda: sys.modules.__setitem__("openai", old) if old is not None
                        else sys.modules.pop("openai", None))
        return captured

    def _set_env(self, name, value):
        old = os.environ.get(name)
        os.environ[name] = value
        self.addCleanup(lambda: os.environ.__setitem__(name, old) if old is not None
                        else os.environ.pop(name, None))

    def test_openai_runner_passes_base_url_and_keyenv(self):
        captured = self._install_fake_openai()
        self._set_env("MY_KEY", "k-123")
        R.OpenAIRunner("m", "/skill", base_url="http://local/v1/", api_key_env="MY_KEY")
        self.assertEqual(captured["kwargs"].get("base_url"), "http://local/v1/")
        self.assertEqual(captured["kwargs"].get("api_key"), "k-123")

    def test_make_runner_gemini_targets_google_endpoint(self):
        import run_evals  # repo root is on sys.path
        captured = self._install_fake_openai()
        self._set_env("GEMINI_API_KEY", "g-key")
        args = types.SimpleNamespace(runner="gemini", skill_dir="/skill", temperature=0.0,
                                     competitor_dir=None, base_url=None, api_key_env="OPENAI_API_KEY")
        runner = run_evals.make_runner(args, None)
        self.assertEqual(runner.model, "gemini-2.5-pro")
        self.assertEqual(captured["kwargs"]["base_url"], run_evals.GEMINI_BASE_URL)
        self.assertEqual(captured["kwargs"]["api_key"], "g-key")

    def test_make_runner_gemini_base_url_override(self):
        import run_evals
        captured = self._install_fake_openai()
        self._set_env("GEMINI_API_KEY", "g-key")
        args = types.SimpleNamespace(runner="gemini", skill_dir="/skill", temperature=0.0,
                                     competitor_dir=None, base_url="http://proxy/v1/",
                                     api_key_env="OPENAI_API_KEY")
        run_evals.make_runner(args, "gemini-2.5-flash")
        self.assertEqual(captured["kwargs"]["base_url"], "http://proxy/v1/")


if __name__ == "__main__":
    unittest.main()
