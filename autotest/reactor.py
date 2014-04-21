# -*- coding: utf-8 -*-

# $Id$

from __future__ import print_function
from datetime import datetime
import sys

from blessings import Terminal


counter = 0

def react(code, output, stdout=sys.stdout):
    """Displays the outcome.

    Displays the ``output`` variable. If ``code`` is zero (no error)
    displays an 'OK' message on green otherwise an 'ERROR' message on
    red.

    """
    global counter
    counter += 1
    t = Terminal(stream=stdout)
    width = t.width if t.is_tty else 80 # when testing t.width is None
    if code:
        formatter = t.bold_white_on_red
        message = "ERROR"
    else:
        formatter = t.bold_white_on_green
        message = "OK"
    stamp = "%3i " % counter + datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    message = message.center(width - 1 - len(stamp), " ")

    print(output, file=stdout)
    print("", file=stdout)
    print(formatter(stamp + message), file=stdout)
