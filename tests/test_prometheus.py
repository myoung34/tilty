# -*- coding: utf-8 -*-
from unittest import mock

from tilty.emitters import prometheus


def test_prometheus_type(
):
    assert prometheus.__type__() == 'Prometheus'


@mock.patch('tilty.emitters.prometheus.push_to_gateway')
def test_prometheus(
    mock_prometheus_client,
):
    config = {
        'url': 'localhost:8000',
        'gravity_gauge_name': 'gravity_g',
        'temp_gauge_name': 'temp_f',
        'labels': '{"color": "{{ color }}"}'
    }
    prometheus.Prometheus(config=config).emit({
        'temp': 80,
        'color': 'black',
        'gravity': 1.054,
        'timestamp': 155558888,
        'mac': 'foo',
    })
    assert mock_prometheus_client.call_count == 1
    assert mock_prometheus_client.call_args[0][0] == 'localhost:8000'
    assert mock_prometheus_client.call_args[1]['job'] == 'tilty'
    registry = mock_prometheus_client.call_args[1]['registry']
    for i, metric in enumerate(registry.collect()):
        assert metric.name in ['gravity_g', 'temp_f']
        if metric.name == 'gravity_g':
            assert metric.samples[0].value == 1.054
        else:
            assert metric.samples[0].value == 80
        assert metric.samples[0].labels['color'] == 'black'
    assert i == 1  # => 2 iterations
