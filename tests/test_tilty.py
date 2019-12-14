# -*- coding: utf-8 -*-
from unittest import mock

from tilty import tilt_device


@mock.patch('tilty.blescan.parse_events', return_value=[{'uuid': 'foo', 'major': 2, 'minor': 1}]) # noqa
def test_scan_for_tilt_data(
    bt_events,
):
    t = tilt_device.TiltDevice()
    t.scan_for_tilt_data()
