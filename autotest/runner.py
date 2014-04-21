# -*- coding: utf-8 -*-

# $Id$

import subprocess
try:
    from subprocess import check_output
except ImportError:
    # backported from python 2.7
    def check_output(*popenargs, **kwargs):
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            excpt = subprocess.CalledProcessError(retcode, cmd)
            excpt.output = output
            raise excpt
        return output


def run(command):
    rcode = 0
    output = ""
    try:
        output = check_output(
            command,
            shell=True,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
    except subprocess.CalledProcessError as e:
        rcode = e.returncode
        output = e.output
    return rcode, output

