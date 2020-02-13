# -*- coding: utf-8 -*-
from unittest import mock

from tilty.emitters import influxdb


@mock.patch('tilty.emitters.influxdb.requests')
def test_influxdb(
    mock_requests,
):
    config = {
        'url': 'http://www.google.com',
        'database': 'foo',
        'temperature_payload': 'temperature,color=Black value=85 1422568543702900257',  # noqa
        'gravity_payload': 'gravity,color=Black value=1.045 1422568543702900257',  # noqa
    }
    influxdb.InfluxDB(config=config).emit()
    assert mock_requests.mock_calls == [
        mock.call.post(
            data='temperature,color=Black value=85 1422568543702900257',
            params=('db', 'mydb'),
            url='http://www.google.com'
        ),
        mock.call.post(
            data='gravity,color=Black value=1.045 1422568543702900257',
            params=('db', 'mydb'),
            url='http://www.google.com'
        )
    ]
