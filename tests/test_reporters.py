# -*- coding: utf-8 -*-

# $Id$

from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from builtins import object

from io import StringIO
import unittest
from future.utils import PY3

if PY3:
    from unittest import mock
else:
    import mock

from arv.autotest.reporters import Repeater
from arv.autotest.reporters import DynamicThrottling
from arv.autotest.reporters import LineAssemblerReporter
from arv.autotest.reporters import TerminalReporter


class TestTerminalReactor(unittest.TestCase):

    def setUp(self):
        self.stdout = StringIO()
        self.reactor = TerminalReporter(self.stdout)

    def tearDown(self):
        self.stdout.close()

    def test_react_on_success(self):
        self.reactor.start()
        self.reactor.feed(b"hello")
        self.reactor.stop(0)
        output = self.stdout.getvalue()
        self.assert_("hello" in output)
        self.assert_("OK" in output)

    def test_react_on_failure(self):
        self.reactor.start()
        self.reactor.feed(b"world")
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
        reactor = LineAssemblerReporter(wrapped)
        reactor.start()
        for i in input:
            reactor.feed(i)
        reactor.stop(0)
        self.assertEqual(wrapped.input, expected)

    def test_preconditions(self):
        wrapped = self.R()
        reactor = LineAssemblerReporter(wrapped)
        self.failIf(wrapped.start_called)
        self.failIf(wrapped.input)
        self.assert_(wrapped.code is None)

    def test_delegates_to_wrapped(self):
        wrapped = self.R()
        reactor = LineAssemblerReporter(wrapped)
        reactor.start()
        reactor.feed(b"hello world")
        reactor.stop(123)
        self.assert_(wrapped.start_called)
        self.assertEqual(wrapped.input, [b"hello world"])
        self.assertEqual(wrapped.code, 123)

    def test_no_input_produces_no_output(self):
        self.assertReactorProduces([], [])
        self.assertReactorProduces([b""], [])

    def test_only_a_newline(self):
        self.assertReactorProduces([b"\n"], [b"\n"])

    def test_no_newline_at_the_end_flushes_remaining_data(self):
        self.assertReactorProduces([b"f", b"o", b"o"], [b"foo"])
        self.assertReactorProduces([b"f", b"o", b"\n", b"o"], [b"fo\n", b"o"])

    def test_newline_at_the_end(self):
        self.assertReactorProduces([b"f", b"o", b"o", b"\n"], [b"foo\n"])

    def test_arbitrary_sized_chunks(self):
        self.assertReactorProduces([b"fo", b"o"], [b"foo"])

    def test_chunks_with_newline(self):
        self.assertReactorProduces([b"f\no", b"o"], [b"f\n", b"oo"])


class TestDynamicThrottlingTimer(unittest.TestCase):

    def set_up(self, times):
        self.throttler = mock.Mock()
        self.timer = mock.Mock(side_effect=times)
        self.reporter = DynamicThrottling(
            self.throttler,
            timer=self.timer
        )

    def test_something(self):
        self.set_up([1, 2])
        self.reporter.start()
        self.reporter.stop(0)
        self.throttler.adjust_delta.assert_called_once_with(1)

    def test_delta_cleared_on_every_run(self):
        self.set_up([1, 2, 4, 7])
        self.reporter.start()
        self.reporter.stop(0)
        self.throttler.adjust_delta.assert_called_with(1)
        self.reporter.start()
        self.reporter.stop(0)
        self.throttler.adjust_delta.assert_called_with(3)


class TestChainReporters(unittest.TestCase):

    def setUp(self):
        self.rpt1 = mock.Mock()
        self.rpt2 = mock.Mock()
        self.chain = Repeater(self.rpt1, self.rpt2)

    def test_start_called(self):
        self.chain.start()
        self.rpt1.start.assert_called_with()
        self.rpt2.start.assert_called_with()

    def test_feed_called(self):
        self.chain.feed("some text")
        self.rpt1.feed.assert_called_with("some text")
        self.rpt2.feed.assert_called_with("some text")

    def test_stop_called(self):
        self.chain.stop(123)
        self.rpt1.stop.assert_called_with(123)
        self.rpt2.stop.assert_called_with(123)
