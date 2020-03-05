# -*- coding: utf-8 -*-
from unittest import mock

from mock_config_parser import MockConfigParser
from tilty import tilt_device, tilty


@mock.patch('tilty.blescan.get_events', return_value=[{'uuid': 'foo', 'major': 2, 'minor': 1}]) # noqa
def test_scan_for_tilt_data(
    bt_events,
):
    t = tilt_device.TiltDevice()
    t.scan_for_tilt_data()
    bt_events.assert_called()


@mock.patch('tilty.emitters.webhook.Webhook')
def test_scan_for_tilt_data_parse_webhook(
    mock_webhook,
):
    config = MockConfigParser('webhook')
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
                'payload': {'color': 'black', 'gravity': 1, 'temp': 32, 'timestamp': '155558888'}  # noqa
            }
        ),
        mock.call().emit()
    ]


@mock.patch('tilty.emitters.influxdb.InfluxDB')
def test_scan_for_tilt_data_parse_influxdb(
    mock_influxdb,
):
    config = MockConfigParser('influxdb')
    tilty.emit(
        config,
        {'color': 'black', 'gravity': 1, 'temp': 32, 'timestamp': 155558888}
    )
    assert mock_influxdb.mock_calls == [
        mock.call(
            config={
                'url': 'http://www.google.com',
                'database': 'foo',
                'temperature_payload': 'temperature,scale=fahrenheit,color=black value=32 155558888',  # noqa
                'gravity_payload': 'gravity,color=black value=1 155558888'
            }
        ),
        mock.call().emit()
    ]


@mock.patch('tilty.emitters.datadog.Datadog')
def test_scan_for_tilt_data_parse_datadog(
    mock_dd,
):
    config = MockConfigParser('datadog')
    tilty.emit(
        config,
        {'color': 'black', 'gravity': 1, 'temp': 32, 'timestamp': 155558888}
    )
    assert mock_dd.mock_calls == [
        mock.call(config={'host': 'http://api.datadog.com', 'port': '8120', 'gravity': 1, 'temperature': 32, 'color': 'black'}),  # noqa
        mock.call().emit()
    ]
