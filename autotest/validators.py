# -*- coding: utf-8 -*-

# $Id$


import os.path

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


def is_list_of(item_validator):
    def validator(value):
        return map(item_validator, value)
    return validator

is_bool = make_validator_from_class(bool)
is_dir = make_validator_from_predicate(os.path.isdir)
is_int = make_validator_from_class(int)
is_str = make_validator_from_class(str)
is_unicode = make_validator_from_class(unicode)
