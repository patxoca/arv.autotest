# -*- coding: utf-8 -*-

# $Id$

"""This module defines some filters and filter factories.

A filter is any callable that receives a :py:class:`pyinotify.Event`
and returns a boolean value.

The :py:class:`~autotest.main.EventHandler` class takes a filter as
argument in order to decide what events we are interested in.

"""

import pyinotify


def is_delete_dir_event(event):
    """Return ``True`` if deleting a directory.
    """
    P = pyinotify
    mask = event.mask
    return bool(
        (mask & P.IN_DELETE) and (mask & (P.IN_DELETE_SELF | P.IN_ISDIR))
        )


class simple_event_filter_factory(object):
    """Factory to create simple filters.

    Instances of this class behave as event filters.

    The constructor accepts a list of *watches*, each one defining how
    the filter should behave with regard to events triggered within a
    folder and its subfolders. Each watch has the properties defined
    by the :py:data:`~autotest.config.WATCH_NODE_SCHEMA` schema.

    * a watch can be any object providing ``getattr``-like access to
      the properties.

    * a watch applied to a directory takes precedence over a watch
      applied to a parent directory.

    * exclusion rules are processed before inclusion rules.

    Instances of this class return ``True`` if the event is *included*
    according to the rules defined by the watches, ``False``
    otherwise.

    """
    def __init__(self, watches):
        w = list(watches)
        # sort the watches by descending path length to make sure that
        # watches on subdirs are processed before its parents
        w.sort(key=lambda x : -len(x.path))
        self._watches = w

    def __call__(self, event):
        container = self._get_container(event.path)
        if container is None:
            # @TODO: alex 2014-04-20 17:03:44 : no hauria de passar
            # (crec). Possiblement millor raise. Si pot passar millor
            # fer configurable el valor retornat
            return False
        if self._match_any(container.exclude, event.name):
            return False
        if self._match_any(container.include, event.name):
            return True
        return False

    def _get_container(self, path):
        for w in self._watches:
            if path.startswith(w.path):
                return w
        return None

    def _match_any(self, re_list, name):
        # @TODO: alex 2014-04-20 17:32:33 : si un name es tingut en
        # compte/ignorat una vegada ho serà sempre (segurament), no
        # cal comprovar novament totes les re. Un mecanísme de cache
        # ho acceleraria.
        for r in re_list:
            if r.match(name):
                return True
        return False


def and_(*filters):
    """Factory *anding* some filters together.
    """
    def filter(event):
        for f in filters:
            if not f(event):
                return False
        return True
    return filter

def not_(filter):
    """Factory *negating* a filter.
    """
    def f(event):
        return not filter(event)
    return f