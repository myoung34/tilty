# -*- coding: utf-8 -*-
from unittest import mock

from tilty import tilt_device, tilty
from mock_config_parser import MockConfigParser


@mock.patch('tilty.blescan.parse_events', return_value=[{'uuid': 'foo', 'major': 2, 'minor': 1}]) # noqa
def test_scan_for_tilt_data(
    bt_events,
):
    t = tilt_device.TiltDevice()
    t.scan_for_tilt_data()



@mock.patch('tilty.emitters.webhook.Webhook')
def test_scan_for_tilt_data(
    mock_webhook,
):
    config = MockConfigParser()
    tilty.emit(
        config,
        {'color': 'black', 'gravity': 1, 'temp': 32, 'timestamp': 155558888}
    )
    assert mock_webhook.mock_calls == [
        mock.call(
            config={
                'url': 'http://www.google.com',
                'headers': {'Content-Type': 'application/json'},
                'method': 'GET',
                'payload': {'color': 'black', 'gravity': 1, 'temp': 32, 'timestamp': '155558888'}
            }
        ),
        mock.call().emit()
    ]
