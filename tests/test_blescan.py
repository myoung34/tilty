# -*- coding: utf-8 -*-
from tilty import blescan


def test_string_packet():
    assert blescan.string_packet(b'\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00') == 'fe000000000000000000000000000000'  # noqa
    assert blescan.string_packet(b'\x93\xe2\xfdD\x1b\xafhOH\xef>mn\x91\xcb\x14') == '93e2fd441baf684f48ef3e6d6e91cb14'  # noqa


def test_packed_bdaddr_to_string():
    assert blescan.packed_bdaddr_to_string(b'ID\x8b\xea&b') == '62:26:ea:8b:44:49'  # noqa


def test_parse_packet():
    assert blescan.parse_packet(b'\x04>+\x02\x01\x03\x01r\xed\x08S\x84=\x1f\x1e\xff\x06\x00\x01\t \x02)\xa7\x93\xe2\xfdD\x1b\xafhOH\xef>mn\x91\xcb\x14\x02$\x98\xc7\xef\xb3') == {'mac': 'ed:72:01:03:01:02', 'uuid': '93e2fd441baf684f48ef3e6d6e91cb14', 'major': 548, 'minor': 39111}  # noqa
    assert blescan.parse_packet(b'\x04>*\x02\x01\x03\x01w\t\xbc\xd0W\xef\x1e\x02\x01\x04\x1a\xffL\x00\x02\x15\xa4\x95\xbb0\xc5\xb1KD\xb5\x12\x13p\xf0-t\xde\x00B\x03\xf7\xc5\xa7') == {'mac': '09:77:01:03:01:02', 'uuid': 'a495bb30c5b14b44b5121370f02d74de', 'major': 66, 'minor': 1015}  # noqa
