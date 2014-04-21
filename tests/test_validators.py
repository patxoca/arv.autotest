# -*- coding: utf-8 -*-

# $Id$


import re
import unittest

from autotest import validators as V
from autotest.utils import NoDefault
from autotest.utils import TypedObject


class TestMakeValidatorFromPredicate(unittest.TestCase):

    def setUp(self):
        def odd(value):
            return bool(value % 2)
        self.validator = V.make_validator_from_predicate(odd)

    def test_passing_validator(self):
        self.assertEqual(self.validator(3), 3)

    def test_failing_validator(self):
        self.assertRaises(
            ValueError,
            self.validator, 2
        )


class TestMakeValidatorFromClass(unittest.TestCase):

    def setUp(self):
        self.validator = V.make_validator_from_class(int)

    def test_passing_validator(self):
        self.assertEqual(self.validator(2), 2)

    def test_failing_validator(self):
        self.assertRaises(ValueError, self.validator, "2")


class TestMakeValidatorFromSchema(unittest.TestCase):

    def setUp(self):
        self.schema = {
            "command": (NoDefault, V.is_str),
            "verbosity": (0, V.is_int),
        }
        self.validator = V.make_validator_from_schema(self.schema)

    def test_passing_validator(self):
        value = {
            "command" : b"echo 1",
            "verbosity" : 2
        }
        result = self.validator(value)
        self.assert_(isinstance(result, TypedObject))
        self.assertEqual(result.command, b"echo 1")
        self.assertEqual(result.verbosity, 2)

    def test_failing_validator(self):
        value = {
            "command" : None,
            "verbosity" : 2
        }
        self.assertRaises(ValueError, self.validator, value)


class TestIsListOf(unittest.TestCase):

    def setUp(self):
        self.validator = V.is_list_of(V.is_int)

    def test_passing_validator(self):
        value = [1, 2, 3]
        self.assertEqual(self.validator(value), value)

    def test_failing_validator(self):
        self.assertRaises(
            ValueError,
            self.validator, [1, "1"]
        )


class TestCompose(unittest.TestCase):

    def setUp(self):
        def increment(value):
            return value + 1
        def double(value):
            return value * 2
        self.increment = increment
        self.double = double

    def test_composition_1(self):
        f = V.compose(self.increment, self.double)
        self.assertEqual(f(2), 6)

    def test_composition_2(self):
        f = V.compose(self.double, self.increment)
        self.assertEqual(f(2), 5)


class TestValidators(unittest.TestCase):

    def test_passing_is_bool(self):
        value = True
        self.assertEqual(V.is_bool(value), value)

    def test_failing_is_bool(self):
        self.assertRaises(ValueError, V.is_bool, 2)

    def test_passing_is_dir(self):
        value = "/tmp"
        self.assertEqual(V.is_dir(value), value)

    def test_failing_is_dir(self):
        self.assertRaises(ValueError, V.is_dir, "/i/hope/it/does/not/exist")

    def test_passing_is_int(self):
        value = 2
        self.assertEqual(V.is_int(value), value)

    def test_failing_is_int(self):
        self.assertRaises(ValueError, V.is_int, "2")

    def test_passing_is_str(self):
        value = b"2"
        self.assertEqual(V.is_str(value), value)

    def test_failing_is_str(self):
        self.assertRaises(ValueError, V.is_str, 2)

    def test_passing_is_unicode(self):
        value = u"2"
        self.assertEqual(V.is_unicode(value), value)

    def test_failing_is_unicode(self):
        self.assertRaises(ValueError, V.is_unicode, 2)

    def test_passing_is_regex(self):
        value = u"test.*\.py"
        result = V.is_regex(value)
        self.assert_(hasattr(result, "match"))
        self.assert_(callable(result.match))
        self.assert_(result.match("test_foo.py"))

    def test_failing_is_regex(self):
        self.assertRaises(ValueError, V.is_regex, 2)

    def test_regex_matches_whole_name(self):
        result = V.is_regex(u"test.*\.py")
        self.failIf(result.match("test_foo.py_garbage"))
        self.failIf(result.match("garbage_test_foo.py"))
