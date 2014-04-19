# -*- coding: utf-8 -*-

# $Id$

from datetime import datetime

from blessings import Terminal


t = Terminal()
counter = 0

def react(code, output):
    """Displays the outcome.

    Displays the ``output`` variable. If ``code`` is zero (no error)
    displays an 'OK' message on green otherwise an 'ERROR' message on
    red.

    """
    global counter
    counter += 1
    if code:
        formatter = t.bold_white_on_red
        message = "ERROR"
    else:
        formatter = t.bold_white_on_green
        message = "OK"
    stamp = "%3i " % counter + datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    message = message.center(t.width - 1 - len(stamp), " ")

    print output
    print
    print formatter(stamp + message)
