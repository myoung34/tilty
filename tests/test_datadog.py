# -*- coding: utf-8 -*-
from unittest import mock

from tilty.emitters import datadog


@mock.patch('tilty.emitters.datadog.statsd')
@mock.patch('tilty.emitters.datadog.initialize')
def test_datadog(
    mock_statsd_init,
    mock_statsd_client,
):
    config = {
        'host': 'http://statsd.google.com',
        'port': '8130',
    }
    tilt_data = {
        'temperature': '55',
        'gravity': '1054',
        'color': 'black',
        'mac': '00:0a:95:9d:68:16',
    }
    datadog.Datadog(config=config).emit(tilt_data)
    mock_statsd_init.mock_calls == [
        mock.call(statsd_host='http://statsd.google.com', statsd_port='8130')
    ]
    assert mock_statsd_client.mock_calls == [
        mock.call.gauge(
            'tilty.temperature',
            '55',
            tags=['color:black', 'mac:00:0a:95:9d:68:16']
        ),
        mock.call.gauge(
            'tilty.gravity',
            '1054',
            tags=['color:black', 'mac:00:0a:95:9d:68:16']
        ),
    ]
