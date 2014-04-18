# -*- coding: utf-8 -*-

# $Id$

from blessings import Terminal


t = Terminal()

def react(code, output):
    print output
    print
    if code:
        print t.bold_white_on_red("ERROR".center(79, " "))
    else:
        print t.bold_white_on_green("OK".center(79, " "))
