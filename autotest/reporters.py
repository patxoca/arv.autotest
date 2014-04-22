# -*- coding: utf-8 -*-

# $Id$

"""A *reporter* is a class intended to consume the output produced by
a *runner*. Usually a reporter will produce output for human
consumption but it may as well act as a filter for other reporters.

A reporter must define three methods:

:start(): called at the beggining.

:feed(data): process a chunk of data produced by the runner.

:stop(return_code): the runner has finished with ``return_code``.

"""

from __future__ import print_function
from datetime import datetime
import sys

from blessings import Terminal


class LineAssemblerReporter(object):
    """Assembles data into lines.

    The purpose of this reporter is assembling chunks of data into
    lines and then feeding them to a wrapped reporter one line at a
    time.

    """

    def __init__(self, wrapped):
        self._wrapped = wrapped
        self._data = []

    def start(self):
        self._wrapped.start()

    def feed(self, data):
        while "\n" in data:
            left, data = data.split("\n", 1)
            self._data.append(left)
            self._data.append("\n")
            self._feed_wrapped()
        if data:
            self._data.append(data)

    def stop(self, code):
        if self._data:
            self._feed_wrapped()
        self._wrapped.stop(code)

    def _feed_wrapped(self):
        self._wrapped.feed("".join(self._data))
        self._data = []


class TerminalReporter(object):
    """Displays data to a terminal.

    This reporter displays the received data into a terminal. On stop
    displays a highlighted message: green indicates success and red
    error.

    """

    def __init__(self, stdout=sys.stdout):
        self.stdout = stdout
        self.term = Terminal(stream=stdout)
        self.counter = 0
        self.width = self.term.width if self.term.is_tty else 80 # when testing t.width is None

    def start(self):
        self.counter += 1

    def feed(self, line):
        print(line, file=self.stdout, end="")

    def stop(self, code):
        if code:
            formatter = self.term.bold_white_on_red
            message = "ERROR"
        else:
            formatter = self.term.bold_white_on_green
            message = "OK"
        stamp = "%3i " % self.counter + datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        message = message.center(self.width - 1 - len(stamp), " ")

        print("", file=self.stdout)
        print(formatter(stamp + message), file=self.stdout)


def make_reporter(**kwargs):
    return LineAssemblerReporter(TerminalReporter(**kwargs))
