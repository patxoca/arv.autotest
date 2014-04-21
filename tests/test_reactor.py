# -*- coding: utf-8 -*-

# $Id$


import unittest

import six

from autotest.reactor import LineAssemblerReactor
from autotest.reactor import TerminalReactor


class TestTerminalReactor(unittest.TestCase):

    def setUp(self):
        self.stdout = six.StringIO()
        self.reactor = TerminalReactor(self.stdout)

    def tearDown(self):
        self.stdout.close()

    def test_react_on_success(self):
        self.reactor.start()
        self.reactor.feed("hello")
        self.reactor.stop(0)
        output = self.stdout.getvalue()
        self.assert_("hello" in output)
        self.assert_("OK" in output)

    def test_react_on_failure(self):
        self.reactor.start()
        self.reactor.feed("world")
        self.reactor.stop(1)
        output = self.stdout.getvalue()
        self.assert_("world" in output)
        self.assert_("ERROR" in output)


class TestLineAssemblerReactor(unittest.TestCase):

    def setUp(self):
        class R(object):
            def __init__(self):
                self.start_called = False
                self.input = []
                self.code = None
            def start(self):
                self.start_called = True
            def feed(self, data):
                self.input.append(data)
            def stop(self, code):
                self.code = code
        self.R = R

    def assertReactorProduces(self, input, expected):
        wrapped = self.R()
        reactor = LineAssemblerReactor(wrapped)
        reactor.start()
        for i in input:
            reactor.feed(i)
        reactor.stop(0)
        self.assertEqual(wrapped.input, expected)

    def test_preconditions(self):
        wrapped = self.R()
        reactor = LineAssemblerReactor(wrapped)
        self.failIf(wrapped.start_called)
        self.failIf(wrapped.input)
        self.assert_(wrapped.code is None)

    def test_delegates_to_wrapped(self):
        wrapped = self.R()
        reactor = LineAssemblerReactor(wrapped)
        reactor.start()
        reactor.feed("hello world")
        reactor.stop(123)
        self.assert_(wrapped.start_called)
        self.assertEqual(wrapped.input, ["hello world"])
        self.assertEqual(wrapped.code, 123)

    def test_no_input_produces_no_output(self):
        self.assertReactorProduces([], [])
        self.assertReactorProduces([""], [])

    def test_only_a_newline(self):
        self.assertReactorProduces(["\n"], ["\n"])

    def test_no_newline_at_the_end_flushes_remaining_data(self):
        self.assertReactorProduces(["f", "o", "o"], ["foo"])
        self.assertReactorProduces(["f", "o", "\n", "o"], ["fo\n", "o"])

    def test_newline_at_the_end(self):
        self.assertReactorProduces(["f", "o", "o", "\n"], ["foo\n"])

    def test_arbitrary_sized_chunks(self):
        self.assertReactorProduces(["fo", "o"], ["foo"])

    def test_chunks_with_newline(self):
        self.assertReactorProduces(["f\no", "o"], ["f\n", "oo"])
