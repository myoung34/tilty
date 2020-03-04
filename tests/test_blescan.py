# -*- coding: utf-8 -*-
from tilty import blescan


def test_number_packet():
    assert blescan.number_packet(b'\x89=') == 35133


def test_string_packet():
    assert blescan.string_packet(b'\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') == 'fe000000000000000000000000000000'  # noqa


def test_packed_bdaddr_to_string():
    assert blescan.packed_bdaddr_to_string(b'ID\x8b\xea&b') == '62:26:ea:8b:44:49'  # noqa
