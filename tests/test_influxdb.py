# -*- coding: utf-8 -*-
from unittest import mock

from tilty.emitters import influxdb


def test_influxdb_type(
):
    assert influxdb.__type__() == 'InfluxDB'


@mock.patch('tilty.emitters.influxdb.InfluxDBClient')
def test_influxdb(
    mock_influx_client,
):
    config = {
        'url': 'http://www.google.com',
        'database': 'foo',
        'gravity_payload_template': '{"measurement": "gravity", "tags": {"color": "{{ color }}"}, "fields": {"value": {{ gravity }}}}',  # noqa
        'temperature_payload_template': '{"measurement": "temperature", "tags": {"color": "{{ color }}"}, "fields": {"value": {{ temp }}}}',  # noqa
    }
    influxdb.InfluxDB(config=config).emit({
        'temp': 80,
        'color': 'black',
        'gravity': 1.054,
        'timestamp': 155558888,
        'mac': 'foo',
    })
    assert mock_influx_client.mock_calls == [
        mock.call('http://www.google.com', 80, None, None, 'foo'),
        mock.call().write_points([
            {
                'measurement': 'temperature',
                'tags': {'color': 'black'},
                'fields': {'value': 80}
            }
        ]),
        mock.call().write_points([
            {
                'measurement': 'gravity',
                'tags': {'color': 'black'},
                'fields': {'value': 1.054}
            }
        ])
    ]
