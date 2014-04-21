# -*- coding: utf-8 -*-

# $Id$


import unittest

import six

from autotest.reactor import react


class TestReactor(unittest.TestCase):

    def setUp(self):
        self.stdout = six.StringIO()

    def tearDown(self):
        self.stdout.close()

    def test_react_on_success(self):
        react(0, "hello", stdout=self.stdout)
        output = self.stdout.getvalue()
        self.assert_("hello" in output)
        self.assert_("OK" in output)

    def test_react_on_failure(self):
        react(1, "world", stdout=self.stdout)
        output = self.stdout.getvalue()
        self.assert_("world" in output)
        self.assert_("ERROR" in output)

