# -*- coding: utf-8 -*-
"""test_utils.py —— 纯工具函数单元测试。"""
import unittest

from dockbuddy_common import (default_seed, env_float, normalize_pdb_id,
                              resolve_device, run_cmd)


class TestUtils(unittest.TestCase):
    def test_normalize_pdb_id(self):
        self.assertEqual(normalize_pdb_id("1abc"), "1ABC")
        self.assertEqual(normalize_pdb_id("  5xjh "), "5XJH")
        self.assertEqual(normalize_pdb_id(""), "")

    def test_default_seed(self):
        self.assertEqual(default_seed(), 42)

    def test_env_float(self):
        self.assertEqual(env_float("NONEXIST_VAR_XYZ", 3.14), 3.14)

    def test_resolve_device_explicit(self):
        self.assertEqual(resolve_device("cpu"), "cpu")

    def test_run_cmd(self):
        r = run_cmd(["python", "-c", "print('hi')"])
        self.assertIn("hi", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
