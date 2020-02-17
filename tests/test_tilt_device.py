# -*- coding: utf-8 -*-
from unittest import mock

from tilty import tilt_device


@mock.patch('tilty.blescan.hci_disable_le_scan')
def test_scan_for_tilt_data(
    mock_disable_le_scan,
):
    t = tilt_device.TiltDevice()
    t.stop()
    mock_disable_le_scan.assert_called()
