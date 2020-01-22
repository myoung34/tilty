# -*- coding: utf-8 -*-
from unittest import mock

import pytest

from tilty.emitters import webhook


@mock.patch('tilty.emitters.webhook.METHODS')
def test_webhook_get(
    mock_requests,
):
    config = {
        'url': 'http://www.google.com',
        'headers': {'Content-Type': 'application/json'},
        'payload': {'b': 'b1'}, 'method': 'GET'
    }
    webhook.Webhook(config=config).emit()
    assert mock_requests.mock_calls == [
        mock.call.get('GET'),
        mock.call.get()(
            json={'b': 'b1'},
            headers={'Content-Type': 'application/json'},
            url='http://www.google.com'
        )
    ]


def test_webhook_invalid_method():
    config = {
        'url': 'http://www.google.com',
        'headers': {'Content-Type': 'application/json'},
        'payload': {'b': 'b1'}, 'method': 'bad'
    }
    with pytest.raises(TypeError):
        webhook.Webhook(config=config).emit()
