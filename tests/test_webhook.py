# -*- coding: utf-8 -*-
import datetime
from unittest import mock

import pytest

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
        ),
        mock.call.get()().raise_for_status(),
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
    black_tilt_mac = '00:0a:95:9d:68:16'
    blue_tilt_mac = '00:0a:95:9d:68:17'
    wh = webhook.Webhook(config=config)
    # On init, we load delay_minutes from config
    assert wh.delay_minutes == 3
    # delay_until is unset until emitting calling emit once
    delay_until = wh.delay_until.get(black_tilt_mac)
    assert delay_until is None
    wh.emit({
        'color': 'black',
        'gravity': 1,
        'temp': 32,
        'mac': black_tilt_mac,
        'timestamp': 155558888
    })
    wh.emit({
        'color': 'black',
        'gravity': 2,
        'temp': 33,
        'mac': black_tilt_mac,
        'timestamp': 155558899
    })
    now = datetime.datetime.now(datetime.timezone.utc)
    assert wh.delay_minutes == 3
    # delay_until should be set for about 3 minutes from now
    delay_until = wh.delay_until.get(black_tilt_mac)
    assert delay_until is not None and delay_until >= now
    # emitted twice, but the second returned before actually sending a request.
    assert mock_requests.mock_calls == [
        mock.call.get('GET'),
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'black', 'gravity': 1, 'temp': 32}, url='http://example.com')  # noqa
    ]

    # enxure that the blue tilt can send while the black one is waiting
    delay_until = wh.delay_until.get(blue_tilt_mac)
    assert delay_until is None
    wh.emit({
        'color': 'blue',
        'gravity': 99,
        'temp': 99,
        'mac': blue_tilt_mac,
        'timestamp': 155559999
    })
    delay_until = wh.delay_until.get(blue_tilt_mac)
    assert delay_until is not None and delay_until >= now
    assert mock_requests.mock_calls == [
        mock.call.get('GET'),
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'black', 'gravity': 1, 'temp': 32}, url='http://example.com'),  # noqa
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'blue', 'gravity': 99, 'temp': 99}, url='http://example.com')  # noqa
    ]

    # move the clock forward by setting delay_until to the past, which should
    # allow a request to process again
    wh.delay_until[black_tilt_mac] = now - datetime.timedelta(minutes=1)
    wh.emit({
        'color': 'black',
        'gravity': 3,
        'temp': 34,
        'mac': '00:0a:95:9d:68:16',
        'timestamp': 155558899
    })
    # delay_until is once again about 3 minutes in the future
    delay_until = wh.delay_until.get(black_tilt_mac)
    assert delay_until is not None and delay_until >= now
    # we now see the request that was made after the delay timeout
    assert mock_requests.mock_calls == [
        mock.call.get('GET'),
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'black', 'gravity': 1, 'temp': 32}, url='http://example.com'),  # noqa
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'blue', 'gravity': 99, 'temp': 99}, url='http://example.com'),  # noqa
        mock.ANY,
        mock.call.get()(
            headers={'Content-Type': 'application/json'},
            json={'color': 'black', 'gravity': 3, 'temp': 34}, url='http://example.com')  # noqa
    ]
