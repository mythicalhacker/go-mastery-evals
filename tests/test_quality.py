"""Tests for the deterministic quality layer (pure-Python; Go-dependent dims skip).

Run:  python -m unittest discover -s tests
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness import quality as Q  # noqa: E402

_GO = shutil.which("go")
_GOLANGCI = shutil.which("golangci-lint")


class IdiomScoreTest(unittest.TestCase):
    def test_idiom_signal_counted(self):
        d = Q.score_detail('package s\nimport "errors"\nvar _ = errors.Join(nil)\n')
        self.assertIn("errors.Join", d["hits"])
        self.assertNotIn("errors.Join", d["misses"])
        self.assertGreaterEqual(d["score"], 1)

    def test_anti_pattern_penalized(self):
        d = Q.score_detail('package s\nfunc f() { panic("x") }\n')
        self.assertIn("anti:panic", d["hits"])
        self.assertEqual(d["score"], -1)

    def test_presence_counts_at_most_once(self):
        # The same idiom twice still contributes its weight once (presence, not frequency).
        code = 'package s\nimport "errors"\nvar _ = errors.Join(nil)\nvar _ = errors.Join(nil)\n'
        self.assertEqual(Q.score_detail(code)["score"], 1)

    def test_signal_in_comment_does_not_count(self):
        # strip_comments contract: a token mentioned only in a comment is not credited.
        case = {"quality_signals": {"positive": [{"pattern": r"ReadTimeout", "label": "rt"}]}}
        self.assertEqual(Q.score_detail("package s\n// ReadTimeout matters\n", case)["score"], 0)
        # but the same token in real code (a string literal) IS credited.
        self.assertEqual(Q.score_detail('package s\nvar _ = "ReadTimeout"\n', case)["score"], 1)

    def test_per_case_positive_and_negative_merge(self):
        case = {"quality_signals": {
            "positive": [{"pattern": r"WithoutCancel\(", "label": "wc", "weight": 2}],
            "negative": [{"pattern": r"context\.Background\(", "label": "bg"}]}}
        good = 'package s\nimport "context"\nvar _ = context.WithoutCancel(nil)\n'
        self.assertEqual(Q.score_detail(good, case)["score"], 2)  # weighted positive
        bad = 'package s\nimport "context"\nvar _ = context.Background()\n'
        d = Q.score_detail(bad, case)
        self.assertIn("anti:bg", d["hits"])
        self.assertEqual(d["score"], -1)

    def test_disable_removes_named_global_signal(self):
        self.assertEqual(Q.score_detail("package s\nfunc f() { panic(1) }\n")["score"], -1)
        case = {"quality_signals": {"disable": ["panic"]}}
        self.assertEqual(Q.score_detail("package s\nfunc f() { panic(1) }\n", case)["score"], 0)


class BothPassConditioningTest(unittest.TestCase):
    def test_both_pass_excludes_a_failing_variant(self):
        M = "m"
        q = {
            (M, "c1", "with"): {"mean": 3.0}, (M, "c1", "without"): {"mean": 1.0},   # both pass
            (M, "c2", "with"): {"mean": 2.0}, (M, "c2", "without"): {"mean": 2.0},   # without fails
        }
        rates = {
            (M, "c1", "with"): 1.0, (M, "c1", "without"): 1.0,
            (M, "c2", "with"): 1.0, (M, "c2", "without"): 0.2,  # < 0.6 -> excluded from both-pass
        }
        d_all, d_both, n_both = Q.deltas(q, rates, M)
        self.assertAlmostEqual(d_all, 1.0)    # mean([3-1, 2-2]) = 1.0
        self.assertAlmostEqual(d_both, 2.0)   # only c1 qualifies -> 3-1
        self.assertEqual(n_both, 1)


class MetricsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="qmetrics_"))
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.raw = self.tmp / "raw"
        self.raw.mkdir()

    def _raw(self, name, code):
        (self.raw / name).write_text(code)

    def _results(self, rows):
        p = self.tmp / "results.json"
        p.write_text(json.dumps({"results": rows}))
        return str(p)

    def test_metrics_pass_rate_and_quality(self):
        self._raw("m__c1__with__s0.txt", 'package s\nimport "errors"\nvar _ = errors.Join(nil)\n')
        self._raw("m__c1__without__s0.txt", 'package s\nfunc f() { panic(1) }\n')
        rj = self._results([
            {"model": "m", "case_id": "c1", "variant": "with", "passed": True, "sample": 0},
            {"model": "m", "case_id": "c1", "variant": "without", "passed": False, "sample": 0},
        ])
        mt = Q.metrics(rj, str(self.raw))
        self.assertAlmostEqual(mt["m"]["c1"]["with"]["pass_rate"], 1.0)
        self.assertAlmostEqual(mt["m"]["c1"]["with"]["quality"], 1.0)
        self.assertAlmostEqual(mt["m"]["c1"]["without"]["pass_rate"], 0.0)
        self.assertAlmostEqual(mt["m"]["c1"]["without"]["quality"], -1.0)

    def test_quality_none_when_raw_absent(self):
        rj = self._results([{"model": "m", "case_id": "c1", "variant": "with", "passed": True, "sample": 0}])
        mt = Q.metrics(rj, str(self.tmp / "no-such-raw"))
        self.assertIsNone(mt["m"]["c1"]["with"]["quality"])
        self.assertAlmostEqual(mt["m"]["c1"]["with"]["pass_rate"], 1.0)


class CompositeFormulaTest(unittest.TestCase):
    """The composite arithmetic holds regardless of which dims are available."""

    def test_quality_equals_breakdown(self):
        code = 'package solution\nimport "errors"\nvar _ = errors.Join(nil)\n'
        c = Q.composite(code, None, workroot=tempfile.gettempdir())
        expected = (c["idiom"]
                    - Q.LINT_WEIGHT * (c["lint_issues"] or 0)
                    + (Q.GOFMT_BONUS if c["gofmt_clean"] else 0))
        self.assertAlmostEqual(c["quality"], expected)

    @unittest.skipUnless(_GO, "Go toolchain absent; Go-dependent quality dims skipped")
    def test_gofmt_dimension_runs_with_go(self):
        clean = 'package solution\n\nfunc F() int { return 1 }\n'
        dims = Q.go_dimensions(clean, {"id": "t"}, workroot=tempfile.gettempdir())
        self.assertIsInstance(dims["gofmt_clean"], bool)
        # golangci-lint may or may not be installed; if absent it degrades to None.
        if _GOLANGCI is None:
            self.assertIsNone(dims["lint_issues"])
            self.assertIn("golangci-lint", dims["skipped"])

    @unittest.skipUnless(_GO is None, "only meaningful without Go")
    def test_dims_skip_gracefully_without_go(self):
        dims = Q.go_dimensions("package s\n", {"id": "t"})
        self.assertIsNone(dims["lint_issues"])
        self.assertIsNone(dims["gofmt_clean"])


if __name__ == "__main__":
    unittest.main()
