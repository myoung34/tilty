# -*- coding: utf-8 -*-
from tilty import common


def test_safe_get_key_no_fallback():
    assert common.safe_get_key({}, 'foo') is None


def test_safe_get_key_fallback():
    assert common.safe_get_key({}, 'foo', 'wut') == 'wut'


def test_safe_get_key_valid():
    assert common.safe_get_key({'foo': 'asdf'}, 'foo', 'wut') == 'asdf'
