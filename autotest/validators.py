# -*- coding: utf-8 -*-

# $Id$


import os.path
import re

import six

from autotest.utils import TypedObject


def make_validator_from_predicate(predicate):
    def validator(value):
        if not predicate(value):
            raise ValueError(value)
        return value
    return validator

def make_validator_from_class(class_):
    def validator(value):
        if not isinstance(value, class_):
            raise ValueError(value)
        return value
    return validator

def make_validator_from_schema(schema):
    def validator(value):
        o = TypedObject(schema)
        for k, v in value.items():
            try:
                setattr(o, k, v)
            except AttributeError:
                raise ValueError(value)
        return o
    return validator

def compose(*functions):
    def validator(value):
        for f in functions:
            value = f(value)
        return value
    return validator

def is_list_of(item_validator):
    def validator(value):
        return [item_validator(i) for i in value]
    return validator

is_bool = make_validator_from_class(bool)
is_dir = make_validator_from_predicate(os.path.isdir)
is_int = make_validator_from_class(int)
is_str = make_validator_from_class(six.binary_type)
is_unicode = make_validator_from_class(six.text_type)
is_regex = compose(
    is_unicode,
    lambda x: re.compile(x + "$")
)
