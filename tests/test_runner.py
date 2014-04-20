# -*- coding: utf-8 -*-

# $Id$


import unittest

from autotest.runner import run


class TestRunner(unittest.TestCase):

    def test_exit_code_0(self):
        code, output = run("echo 'hello' && exit 0")
        self.assertEqual(code, 0)
        self.assertEqual(output, "hello\n")

    def test_exit_code_1(self):
        code, output = run("echo 'hello' && exit 1")
        self.assertEqual(code, 1)
        self.assertEqual(output, "hello\n")

