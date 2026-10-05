"""acrostic-poet 单元测试。运行：python3 -m unittest discover -s tests"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from poet import (  # noqa: E402
    make_acrostic, make_haiku, generate, acrostic_with_llm,
)


class TestAcrostic(unittest.TestCase):
    def test_line_count(self):
        lines = make_acrostic("春花开")
        self.assertEqual(len(lines), 3)

    def test_each_starts_with_char(self):
        chars = "春花开"
        lines = make_acrostic(chars)
        for ch, line in zip(chars, lines):
            self.assertTrue(line.startswith(ch))

    def test_unknown_char_fallback(self):
        lines = make_acrostic("曦")
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].startswith("曦"))

    def test_no_chars(self):
        self.assertEqual(make_acrostic("abc 123"), [])


class TestHaiku(unittest.TestCase):
    def test_three_lines(self):
        lines = make_haiku("花")
        self.assertEqual(len(lines), 3)


class TestNoKey(unittest.TestCase):
    def test_fallback_rule(self):
        r = generate("山水", use_llm=True)
        self.assertEqual(r["source"], "rule")
        self.assertEqual(len(r["lines"]), 2)

    def test_llm_none(self):
        self.assertIsNone(acrostic_with_llm("山水"))


if __name__ == "__main__":
    unittest.main()
