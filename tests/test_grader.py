"""Unit tests for the grader's comment-aware idiom matching.

Run:  python -m unittest discover -s tests

These tests are stdlib-only and (except the explicitly-guarded grade() test that
needs no toolchain) do not invoke Go, so they run anywhere.
"""
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.grader import extract_code, grade, strip_comments  # noqa: E402


class ExtractCodeTest(unittest.TestCase):
    def test_self_correction_takes_last_package_block(self):
        # Buggy first block, corrected second block — the final answer wins.
        resp = (
            "Here's an implementation:\n\n"
            "```go\npackage solution\n\nfunc F() int { return 0 } // oops\n```\n\n"
            "Wait, that's wrong. Corrected version:\n\n"
            "```go\npackage solution\n\nfunc F() int { return 42 }\n```\n"
        )
        out = extract_code(resp)
        self.assertIn("return 42", out)
        self.assertNotIn("return 0", out)

    def test_single_block_unchanged(self):
        out = extract_code("```go\npackage solution\n\nvar X = 1\n```")
        self.assertIn("var X = 1", out)

    def test_trailing_nonpackage_block_does_not_displace_answer(self):
        # A trailing block without `package` (e.g. shell output) must not win.
        resp = (
            "```go\npackage solution\n\nvar X = 1\n```\n\n"
            "Run it:\n\n```\n$ go test ./...\nok\n```\n"
        )
        out = extract_code(resp)
        self.assertIn("package solution", out)
        self.assertNotIn("go test", out)

    def test_no_package_falls_back_to_last_block(self):
        out = extract_code("```\nfirst\n```\n\n```\nlast\n```")
        self.assertIn("last", out)
        self.assertNotIn("first", out)

    def test_no_fence_returns_raw_text(self):
        out = extract_code("package solution\n\nvar X = 1\n")
        self.assertIn("package solution", out)


class StripCommentsTest(unittest.TestCase):
    def test_token_only_in_line_comment_is_absent(self):
        out = strip_comments("x := 1 // calls errors.As( here\n")
        self.assertNotIn("errors.As(", out)
        self.assertIn("x := 1", out)

    def test_token_only_in_block_comment_is_absent(self):
        out = strip_comments("a /* uses errors.As( */ b\n")
        self.assertNotIn("errors.As(", out)
        self.assertIn("a", out)
        self.assertIn("b", out)

    def test_double_slash_inside_string_is_not_a_comment(self):
        # "http://x" — the // lives in a string literal and must be preserved.
        out = strip_comments('u := "http://example.com/path"\n')
        self.assertIn('"http://example.com/path"', out)

    def test_raw_string_preserves_slashes_and_verbs(self):
        # Raw string containing // and %w must survive untouched.
        out = strip_comments("q := `SELECT // %w not a comment`\n")
        self.assertIn("// %w not a comment", out)
        self.assertIn("%w", out)

    def test_escaped_quote_in_string_keeps_string_open(self):
        # The \" is an escaped quote, so the // stays inside the string literal.
        out = strip_comments('s := "a\\"// still string"\n')
        self.assertIn("// still string", out)

    def test_rune_escaped_single_quote_is_handled(self):
        # '\'' is a valid rune literal; the trailing // is a real comment.
        out = strip_comments("c := '\\'' // gone\n")
        self.assertIn("'\\''", out)
        self.assertNotIn("gone", out)

    def test_backtick_inside_line_comment_does_not_open_raw_string(self):
        # A stray ` in a comment must not flip us into raw-string state and
        # swallow the following code.
        out = strip_comments("// a ` b\nreal := errors.AsType[int]\n")
        self.assertIn("errors.AsType[int]", out)

    def test_block_comment_preserves_line_count(self):
        src = "a\n/* x\ny\nz */\nb\n"
        self.assertEqual(src.count("\n"), strip_comments(src).count("\n"))

    def test_division_operator_is_not_a_comment(self):
        out = strip_comments("z := a / b / c\n")
        self.assertIn("a / b / c", out)


class GradeCommentAwareTest(unittest.TestCase):
    """grade()'s regex checks run on comment-stripped source (no toolchain needed:
    build/vet/test are all off, so only must_match/must_not_match execute)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="grader_test_")

    def _case(self, checks):
        return {"id": "t", "_dir": self.tmp, "go_version": "1.26", "checks": checks}

    def test_forbidden_token_only_in_comment_passes(self):
        case = self._case({"build": False, "must_not_match": [r"errors\.As\("]})
        code = "package solution\n// legacy used errors.As( long ago\nvar X = 1\n"
        self.assertTrue(grade(case, code, "t", self.tmp).passed)

    def test_forbidden_token_in_real_code_fails(self):
        case = self._case({"build": False, "must_not_match": [r"errors\.As\("]})
        code = "package solution\nvar _ = errors.As(err, &x)\n"
        self.assertFalse(grade(case, code, "t", self.tmp).passed)

    def test_required_token_only_in_comment_is_not_credited(self):
        case = self._case({"build": False, "must_match": [r"cmp\.Or"]})
        code = "package solution\n// should use cmp.Or here\nvar X = 1\n"
        self.assertFalse(grade(case, code, "t", self.tmp).passed)

    def test_required_token_in_string_literal_is_credited(self):
        # %w in a format string is real, matchable code — not a comment.
        case = self._case({"build": False, "must_match": [r"%w"]})
        code = 'package solution\nvar _ = fmt.Errorf("ctx: %w", err)\n'
        self.assertTrue(grade(case, code, "t", self.tmp).passed)


_GO = shutil.which("go") or (
    os.path.join(os.environ["GOROOT"], "bin", "go")
    if os.environ.get("GOROOT") and os.path.exists(os.path.join(os.environ["GOROOT"], "bin", "go"))
    else None
)


@unittest.skipUnless(_GO, "Go toolchain not on PATH; integration grade() tests skipped")
class ToolchainIntegrationTest(unittest.TestCase):
    """Exercise the toolchain-integration layer of grade() — the paths where every
    late-surfacing harness bug actually lived (package normalization, subprocess
    decode, build-vs-test, extra test files). The text-layer tests above never
    invoke Go, which is exactly why these bugs hid: nothing executed this layer.
    Each test reproduces one real bug so a regression can't sneak back.
    """

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="grader_itest_")
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def _case(self, checks, package="solution"):
        return {"id": "t", "_dir": self.tmp, "go_version": "1.26",
                "package": package, "filename": "solution.go", "checks": checks}

    def _write(self, name, content):
        p = Path(self.tmp) / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)

    def test_alt_package_name_is_normalized(self):
        # A model that emits `package main` must still grade on its logic, not die
        # with "found packages main and solution". (Niche-case package collision.)
        self._write("test.go",
                    'package solution\nimport "testing"\n'
                    'func TestF(t *testing.T){ if F()!=42 {t.Fatalf("got %d", F())} }\n')
        code = "package main\n\nfunc F() int { return 42 }\n"
        self.assertTrue(grade(self._case({"build": True, "test": True}), code, "t", self.tmp).passed)

    def test_non_utf8_test_output_does_not_crash(self):
        # A test that writes invalid UTF-8 then fails must yield a FAIL result, not
        # raise UnicodeDecodeError. (Aider decode crash.)
        self._write("test.go",
                    'package solution\nimport ("os"; "testing")\n'
                    'func TestX(t *testing.T){ os.Stdout.Write([]byte{0xff,0xfe,0x80}); t.Fatal("boom") }\n')
        try:
            r = grade(self._case({"build": False, "test": True}), "package solution\n", "t", self.tmp)
        except UnicodeDecodeError as e:  # pragma: no cover
            self.fail(f"grade() crashed on non-UTF-8 output: {e}")
        self.assertFalse(r.passed)

    def test_build_excludes_test_helpers_but_test_includes_them(self):
        # A solution using a helper defined in the test file builds only under
        # `go test`, not `go build`. Locks the build-vs-test distinction that made
        # a standalone build wrongly fail valid solutions. (bottle-song.)
        self._write("test.go",
                    'package solution\nimport "testing"\n'
                    'func helper() int { return 42 }\n'
                    'func TestF(t *testing.T){ if F()!=helper() {t.Fatal("no")} }\n')
        code = "package solution\n\nfunc F() int { return helper() }\n"
        self.assertFalse(grade(self._case({"build": True}), code, "t", self.tmp).passed)
        self.assertTrue(grade(self._case({"build": False, "test": True}), code, "t", self.tmp).passed)

    def test_extra_test_file_in_files_dir_is_compiled(self):
        # cases_test.go-style extra test files routed via files/ must compile with
        # the main test. (Multi-test-file aider exercises.)
        self._write("test.go",
                    'package solution\nimport "testing"\n'
                    'func TestF(t *testing.T){ if F()!=data() {t.Fatal("no")} }\n')
        self._write("files/extra_test.go", "package solution\n\nfunc data() int { return 7 }\n")
        code = "package solution\n\nfunc F() int { return 7 }\n"
        self.assertTrue(grade(self._case({"build": False, "test": True}), code, "t", self.tmp).passed)


if __name__ == "__main__":
    unittest.main()
