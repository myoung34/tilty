# -*- coding: utf-8 -*-
from unittest import mock

import pytest
import datetime

from tilty.emitters import webhook


def test_webhook_type(
):
    assert webhook.__type__() == 'Webhook'


@mock.patch('tilty.emitters.webhook.METHODS')
def test_webhook_get(
    mock_requests,
):
    config = {
        'url': 'http://www.google.com',
        'headers': '{"Content-Type": "application/json"}',
        'payload_template': '{"color": "{{ color }}", "gravity": {{ gravity }}, "temp": {{ temp }}}',  # noqa
        'method': 'GET',
    }
    webhook.Webhook(config=config).emit({
        'color': 'black',
        'gravity': 1,
        'temp': 32,
        'mac': '00:0a:95:9d:68:16',
        'timestamp': 155558888
    })
    assert mock_requests.mock_calls == [
        mock.call.get('GET'),
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'black', 'gravity': 1, 'temp': 32}, url='http://www.google.com')  # noqa
    ]


@mock.patch('tilty.emitters.webhook.METHODS')
def test_webhook_post_json(
    mock_requests,
):
    config = {
        'url': 'http://www.google.com',
        'headers': '{"Content-Type": "application/json"}',
        'payload_template': '{"color": "{{ color }}", "gravity": {{ gravity }}, "temp": {{ temp }}}',  # noqa
        'method': 'POST',
    }
    webhook.Webhook(config=config).emit({
        'color': 'black',
        'gravity': 1,
        'temp': 32,
        'mac': '00:0a:95:9d:68:16',
        'timestamp': 155558888
    })
    assert mock_requests.mock_calls == [
        mock.call.get('POST'),
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'black', 'gravity': 1, 'temp': 32},
            url='http://www.google.com'
        )
    ]


@mock.patch('tilty.emitters.webhook.METHODS')
def test_webhook_post_data(
    mock_requests,
):
    config = {
        'url': 'http://www.google.com',
        'headers': '{"Content-Type": "text/plain"}',
        'payload_template': '{"color": "{{ color }}", "gravity": {{ gravity }}, "temp": {{ temp }}, "timestamp": "{{ timestamp }}"}',  # noqa
        'method': 'POST',
    }
    webhook.Webhook(config=config).emit({
        'color': 'black',
        'gravity': 1,
        'temp': 32,
        'mac': '00:0a:95:9d:68:16',
        'timestamp': 155558888
    })
    assert mock_requests.mock_calls == [
        mock.call.get('POST'),
        mock.ANY,
        mock.call.get()(
            data={'color': 'black', 'gravity': 1, 'temp': 32, 'timestamp': '155558888'},  # noqa
            headers={'Content-Type': 'text/plain'},
            url='http://www.google.com'
        )
    ]


def test_webhook_invalid_method():
    config = {
        'url': 'http://www.google.com',
        'headers': {'Content-Type': 'application/json'},
        'payload_template': '{"color": "{{ color }}", "gravity": {{ gravity }}, "temp": {{ temp }}, "timestamp": "{{ timestamp }}"}',  # noqa
        'method': 'FOO',
    }
    with pytest.raises(KeyError):
        webhook.Webhook(config=config).emit({
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        })


@mock.patch('tilty.emitters.webhook.METHODS')
def test_webhook_delay_minutes(
    mock_requests,
):
    config = {
        'url': 'http://example.com',
        'headers': '{"Content-Type": "application/json"}',
        'delay_minutes': '3',
        'payload_template': '{"color": "{{ color }}", "gravity": {{ gravity }}, "temp": {{ temp }}}',  # noqa
        'method': 'GET',
    }
    wh = webhook.Webhook(config=config)
    wh.emit({
        'color': 'black',
        'gravity': 1,
        'temp': 32,
        'mac': '00:0a:95:9d:68:16',
        'timestamp': 155558888
    })
    wh.emit({
        'color': 'black',
        'gravity': 2,
        'temp': 33,
        'mac': '00:0a:95:9d:68:16',
        'timestamp': 155558899
    })
    now = datetime.datetime.now(datetime.timezone.utc)
    assert wh.delay_minutes == 3
    assert wh.delay_until is not None
    assert wh.delay_until >= now
    assert mock_requests.mock_calls == [
        mock.call.get('GET'),
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'black', 'gravity': 1, 'temp': 32}, url='http://example.com')  # noqa
    ]

    wh.delay_until = now - datetime.timedelta(minutes=1)
    wh.emit({
        'color': 'black',
        'gravity': 2,
        'temp': 33,
        'mac': '00:0a:95:9d:68:16',
        'timestamp': 155558899
    })
    assert mock_requests.mock_calls == [
        mock.call.get('GET'),
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'black', 'gravity': 1, 'temp': 32}, url='http://example.com'),  # noqa
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'black', 'gravity': 2, 'temp': 33}, url='http://example.com')  # noqa
    ]
