"""Tests for noise-tolerant baseline comparison (pure-Python; no API, no Go).

Run:  python -m unittest discover -s tests
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness import compare_baseline as C  # noqa: E402


def _m(pass_rate, quality=None):
    return {"M": {"c1": {"with": {"pass_rate": pass_rate, "quality": quality}}}}


class ToleranceTest(unittest.TestCase):
    def test_single_sample_flip_within_tol_not_flagged(self):
        # 5/5 -> 4/5 is a 0.2 drop at n=5; NOT > pass-tol 0.2 -> ignored (noise).
        corr, qual, _ = C.compare(_m(1.0), _m(0.8), pass_tol=0.2, quality_tol=0.5)
        self.assertEqual(corr, [])
        self.assertEqual(qual, [])

    def test_real_pass_rate_drop_flagged(self):
        # 5/5 -> 2/5 is a 0.6 drop; > 0.2 -> a real correctness regression.
        corr, qual, _ = C.compare(_m(1.0), _m(0.4), pass_tol=0.2, quality_tol=0.5)
        self.assertEqual(len(corr), 1)
        self.assertEqual(corr[0][:2], ("M", "c1"))

    def test_quality_drop_on_still_passing_case_flagged(self):
        # Still passing (new pass_rate 1.0 >= 0.6) but quality 3.0 -> 1.0 (drop 2.0 > 0.5).
        corr, qual, _ = C.compare(_m(1.0, 3.0), _m(1.0, 1.0), pass_tol=0.2, quality_tol=0.5)
        self.assertEqual(corr, [])
        self.assertEqual(len(qual), 1)
        self.assertEqual(qual[0], ("M", "c1", 3.0, 1.0))

    def test_small_quality_drop_within_tol_not_flagged(self):
        corr, qual, _ = C.compare(_m(1.0, 3.0), _m(1.0, 2.7), pass_tol=0.2, quality_tol=0.5)
        self.assertEqual(qual, [])

    def test_quality_drop_ignored_when_case_no_longer_passes(self):
        # If it stopped passing, correctness flags it; we don't double-count a quality reg.
        corr, qual, _ = C.compare(_m(1.0, 3.0), _m(0.2, 1.0), pass_tol=0.2, quality_tol=0.5)
        self.assertEqual(len(corr), 1)  # correctness regression
        self.assertEqual(qual, [])      # not also a quality regression

    def test_missing_quality_side_is_skipped(self):
        # Old baseline without raw -> quality None -> no quality comparison, no crash.
        corr, qual, _ = C.compare(_m(1.0, None), _m(1.0, 1.0), pass_tol=0.2, quality_tol=0.5)
        self.assertEqual(qual, [])


class EndToEndTest(unittest.TestCase):
    """main() over temp results.json files: a single-sample flip exits 0."""

    def _run_dir(self, root, name, passed_count):
        d = Path(root) / name
        (d / "raw").mkdir(parents=True)
        rows = [{"model": "M", "case_id": "c1", "variant": "with",
                 "passed": i < passed_count, "sample": i} for i in range(5)]
        (d / "results.json").write_text(json.dumps({"results": rows}))
        # one raw sample so quality is defined (idiom: errors.Join -> +1)
        (d / "raw" / "M__c1__with__s0.txt").write_text(
            'package solution\nimport "errors"\nvar _ = errors.Join(nil)\n')
        return d

    def test_flip_exits_zero(self):
        root = tempfile.mkdtemp(prefix="cmp_")
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        base = self._run_dir(root, "base", 5)   # 5/5
        new = self._run_dir(root, "new", 4)      # 4/5 — within tol
        rc = C.main(["compare", str(base), str(new / "results.json"),
                     "--cases-dir", "cases", "--aider-dir", "cases-aider"])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
