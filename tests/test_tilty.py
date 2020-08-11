# -*- coding: utf-8 -*-
from unittest import mock

from mock_config_parser import MockConfigParser
from mock_config_parser_mac import MockConfigParserMac
from tilty import tilt_device, tilty
from tilty.emitters import datadog, influxdb, sqlite, webhook
from tilty.tilty import parse_config


def test_parse_config():

    config = MockConfigParser('sqlite')
    emitters = parse_config(config)
    assert not emitters


@mock.patch('tilty.blescan.get_events', return_value=[{'uuid': 'foo', 'major': 2, 'minor': 1}]) # noqa
def test_scan_for_tilt_data(
    bt_events,
):
    t = tilt_device.TiltDevice()
    t.scan_for_tilt_data()
    bt_events.assert_called()


@mock.patch('tilty.emitters.sqlite.sqlite3')
def test_scan_for_tilt_data_parse_sqlite(
    mock_sqlite,
):
    config = MockConfigParser('sqlite')[0]
    emitter = sqlite.SQLite(config=config)
    tilty.emit(
        emitters=[emitter],
        tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
        }
    )
    assert mock_sqlite.mock_calls == [
        mock.call.connect('/foo.sqlite'),
        mock.call.connect().execute('\n            CREATE TABLE IF NOT EXISTS data(\n              id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n              gravity INTEGER,\n              temp INTEGER,\n              color VARCHAR(16),\n              mac VARCHAR(17),\n              timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)\n        '),  # noqa
        mock.call.connect().execute('insert into data (gravity,temp,color,mac) values (?,?,?,?)', (1, 32, 'black', '00:0a:95:9d:68:16')),  # noqa
        mock.call.connect().commit()
    ]


@mock.patch('tilty.emitters.webhook.Webhook')
def test_scan_for_tilt_data_parse_webhook(
    mock_webhook,
):
    config = MockConfigParser('webhook')[0]
    emitter = webhook.Webhook(config=config)
    tilty.emit(
        emitters=[emitter],
        tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        }
    )
    assert mock_webhook.mock_calls == [
        mock.call(config={
            'url': 'http://www.google.com',
            'headers': '{"Content-Type": "application/json"}',
            'payload_template': '{"color": "{{ color }}", "gravity": {{ gravity }}, "temp": {{ temp }}, "timestamp": "{{ timestamp }}"}',  # noqa
            'method': 'GET'
        }),
        mock.call().emit(tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        })
    ]


@mock.patch('tilty.emitters.webhook.Webhook')
def test_scan_for_tilt_data_parse_webhook_with_mac(
    mock_webhook,
):
    config = MockConfigParserMac('webhook')[0]
    emitter = webhook.Webhook(config=config)
    tilty.emit(
        emitters=[emitter],
        tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        }
    )
    assert mock_webhook.mock_calls == [
        mock.call(config={
            'url': 'http://www.google.com',
            'headers': '{"Content-Type": "application/json"}', 'payload_template': '{"color": "{{ color }}", "gravity": {{ gravity }}, "temp": {{ temp }}, "mac": "{{ mac }}", "timestamp": "{{ timestamp }}"}',  # noqa
            'method': 'GET'
        }),
        mock.call().emit(tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        })
    ]


@mock.patch('tilty.emitters.influxdb.InfluxDB')
def test_scan_for_tilt_data_parse_influxdb(
    mock_influxdb,
):
    config = MockConfigParser('influxdb')[0]
    emitter = influxdb.InfluxDB(config=config)
    tilty.emit(
        emitters=[emitter],
        tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        }
    )
    assert mock_influxdb.mock_calls == [
        mock.call(config={
            'url': 'http://www.google.com',
            'database': 'foo',
            'gravity_payload_template': 'gravity,color={{ color }} value={{ gravity }} {{timestamp}}',  # noqa
            'temperature_payload_template': 'temperature,scale=fahrenheit,color={{ color }} value={{ temp }} {{timestamp}}'  # noqa
        }),
        mock.call().emit(tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        })
    ]


@mock.patch('tilty.emitters.influxdb.InfluxDB')
def test_scan_for_tilt_data_parse_influxdb_with_mac(
    mock_influxdb,
):
    config = MockConfigParserMac('influxdb')[0]
    emitter = influxdb.InfluxDB(config=config)
    tilty.emit(
        emitters=[emitter],
        tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        }
    )
    assert mock_influxdb.mock_calls == [
        mock.call(config={
            'url': 'http://www.google.com',
            'database': 'foo',
            'gravity_payload_template': 'gravity,mac={{ mac }} color={{ color }} value={{ gravity }} {{timestamp}}',  # noqa
            'temperature_payload_template': 'temperature,scale=fahrenheit,mac={{ mac }} color={{ color }} value={{ temp }} {{timestamp}}'  # noqa
        }),
        mock.call().emit(tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        })
    ]


@mock.patch('tilty.emitters.datadog.Datadog')
def test_scan_for_tilt_data_parse_datadog(
    mock_dd,
):
    config = MockConfigParser('datadog')[0]
    emitter = datadog.Datadog(config=config)
    tilty.emit(
        emitters=[emitter],
        tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        }
    )
    assert mock_dd.mock_calls == [
        mock.call(config={
            'host': 'http://api.datadog.com',
            'port': '8120'
        }),
        mock.call().emit(tilt_data={
            'color': 'black',
            'gravity': 1,
            'temp': 32,
            'mac': '00:0a:95:9d:68:16',
            'timestamp': 155558888
        })
    ]
