# -*- coding: utf-8 -*-

# $Id$

ANSI_RED = '\033[30;41;5m'  # blink in xterm
ANSI_GREEN = '\033[30;42;2m'
ANSI_YELLOW = '\033[30;43;2m'
ANSI_NOCOLOR = '\033[0m'

def react(code, output):
    color, message = (ANSI_GREEN, "OK") if not code else (ANSI_RED, "ERROR")
    print output
    print
    print "%s%s%s" % (color, message.center(79, " "), ANSI_NOCOLOR)
