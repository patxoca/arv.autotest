# -*- coding: utf-8 -*-

# $Id$


import os
import re
import shutil
import tempfile
import unittest

import pyinotify

from autotest.config import watch_node_validator
from autotest.filters import and_
from autotest.filters import is_delete_dir_event
from autotest.filters import not_
from autotest.filters import simple_event_filter_factory


class Object(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


def make_event(path, name, mask=0):
    return Object(path=path, name=name, mask=mask)

def make_watch(path, recurse=False, auto_add=False, include=[], exclude=[]):
    return watch_node_validator({
        "path" : path,
        "recurse" : recurse,
        "auto_add" : auto_add,
        "include" : include,
        "exclude" : exclude
    })


class TestIsDirEvent(unittest.TestCase):

    def test_exclude_directory_delete(self):
        event = make_event("", "", pyinotify.IN_DELETE | pyinotify.IN_ISDIR)
        self.assert_(is_delete_dir_event(event))

    def test_exclude_self_delete(self):
        event = make_event("", "", pyinotify.IN_DELETE | pyinotify.IN_DELETE_SELF)
        self.assert_(is_delete_dir_event(event))

    def test_include_directory_create(self):
        event = make_event("", "", pyinotify.IN_CREATE | pyinotify.IN_ISDIR)
        self.failIf(is_delete_dir_event(event))


class TestSimpleEventFilterFactory(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def teadDown(self):
        shutil.rmtree(self.tmpdir)

    def make_subdir(self, name):
        name = os.path.join(self.tmpdir, name)
        os.mkdir(name)
        return name

    def test_exclude_excluded_file(self):
        event = make_event(self.tmpdir, "exclude.abc")
        filter = simple_event_filter_factory([
            make_watch(self.tmpdir, exclude=[u".*\\.abc"])
        ])
        self.failIf(filter(event))

    def test_include_included_file(self):
        event = make_event(self.tmpdir, "include.abc")
        filter = simple_event_filter_factory([
            make_watch(self.tmpdir, include=[u".*\\.abc"])
        ])
        self.assert_(filter(event))

    def test_exclude_excluced_file_in_subdirectory(self):
        subdir = self.make_subdir("subdir")
        event = make_event(subdir, "exclude.abc")
        filter = simple_event_filter_factory([
            make_watch(self.tmpdir, exclude=[u".*\\.abc"])
        ])
        self.failIf(filter(event))

    def test_include_included_file_in_subdirectory(self):
        subdir = self.make_subdir("subdir")
        event = make_event(subdir, "include.abc")
        filter = simple_event_filter_factory([
            make_watch(self.tmpdir, include=[u".*\\.abc"])
        ])
        self.assert_(filter(event))

    def test_exclude_specific_takes_over_generic(self):
        subdir = self.make_subdir("subdir")
        event = make_event(subdir, "exclude.abc")
        filter = simple_event_filter_factory([
            make_watch(self.tmpdir, include=[u".*\\.abc"]), # /tmp
            make_watch(subdir, exclude=[u".*\\.abc"]),      # /tmp/subdir
        ])
        self.failIf(filter(event))

    def test_include_specific_takes_over_generic(self):
        subdir = self.make_subdir("subdir")
        event = make_event(subdir, "exclude.abc")
        filter = simple_event_filter_factory([
            make_watch(self.tmpdir, exclude=[u".*\\.abc"]), # /tmp
            make_watch(subdir, include=[u".*\\.abc"]),      # /tmp/subdir
        ])
        self.assert_(filter(event))

    def test_global_exclude_takes_over_all(self):
        event = make_event(self.tmpdir, ".exclude.abc")
        filter = simple_event_filter_factory(
            watches=[
                make_watch(self.tmpdir, include=[u".*\\.abc"]),
            ],
            global_ignores=[re.compile("\\..*")]
        )
        self.failIf(filter(event))

    def test_neither_excluded_nor_included_gets_excluded_by_default(self):
        event = make_event(self.tmpdir, "exclude.txt")
        filter = simple_event_filter_factory([
            make_watch(self.tmpdir, exclude=[u".*\\.abc"], include=[u".*\\.py"])
            ])
        self.failIf(filter(event))

    def test_unwatched_directory_raises_ValueError(self):
        parent = os.path.dirname(self.tmpdir)
        event = make_event(parent, "exclude.abc")
        filter = simple_event_filter_factory([
            make_watch(self.tmpdir, include=[u".*\\.abc"])
            ])
        self.assertRaises(ValueError, filter, event)


class TestFilterCombinators(unittest.TestCase):

    def setUp(self):
        def is_odd(value):
            return bool(value % 2)
        def is_big(value):
            return value > 100
        self.is_odd = is_odd
        self.is_big = is_big

    def test_preconditions(self):
        self.assert_(self.is_odd(3))
        self.failIf(self.is_odd(2))
        self.assert_(self.is_big(1000))
        self.failIf(self.is_big(2))

    def test_negation(self):
        f = not_(self.is_odd)
        self.assert_(f(2))
        self.failIf(f(3))

    def test_and(self):
        f = and_(self.is_odd, self.is_big)
        self.assert_(f(1003))
        self.failIf(f(1002))
        self.failIf(f(3))
        self.failIf(f(2))
