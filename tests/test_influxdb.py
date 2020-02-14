# -*- coding: utf-8 -*-
from unittest import mock

from tilty.emitters import influxdb


@mock.patch('tilty.emitters.influxdb.InfluxDBClient')
def test_influxdb(
    mock_influx_client,
):
    config = {
        'url': 'http://www.google.com',
        'database': 'foo',
        'gravity_payload': '{"measurement": "gravity", "tags": {"color": "Black"}, "fields": {"value": 1.054}}',  # noqa
        'temperature_payload': '{"measurement": "temperature", "tags": {"color": "Black", "scale": "fahrenheight"}, "fields": {"value": 32}}',  # noqa
    }
    influxdb.InfluxDB(config=config).emit()
    assert mock_influx_client.mock_calls == [
        mock.call(
            'http://www.google.com',
            80,
            None,
            None,
            'foo'
        ),
        mock.call().write_points([
            {
                'measurement': 'temperature',
                'tags': {'color': 'Black', 'scale': 'fahrenheight'},
                'fields': {'value': 32}
            }
        ]),
        mock.call().write_points([
            {
                'measurement': 'gravity',
                'tags': {'color': 'Black'},
                'fields': {'value': 1.054}
            }
        ])
    ]
