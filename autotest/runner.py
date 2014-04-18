# -*- coding: utf-8 -*-

# $Id$

import subprocess

def run(command):
    rcode = 0
    output = ""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        rcode = e.returncode
        output = e.output
    return rcode, output

