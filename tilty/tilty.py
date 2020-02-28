# -*- coding: utf-8 -*-
""" Class to encapsulate all the emitter logic """
import json

from jinja2 import Template

from tilty.emitters import datadog, influxdb, webhook


def emit(config, tilt_data):
    """ Find and call emitters from config

    config (dict): configuration file loaded from disk
    tilt_data (dict): data returned from valid tilt device scan
    """
    if tilt_data is None:
        return
    # <start config sample>
    # [webhook]
    # url = http://www.foo.com
    # self.headers = {"Content-Type": "application/json"}
    # payload_template = {"color": "{{ color }}", "gravity"...
    # method = GET
    if config.has_section('webhook'):
        _template = Template(config['webhook']['payload_template'])
        _config = {
            'url': config['webhook']['url'],
            'headers': json.loads(config['webhook'].get('headers')),
            'method': config['webhook']['method'],
            'payload': json.loads(_template.render(
                color=tilt_data['color'],
                gravity=tilt_data['gravity'],
                temp=tilt_data['temp'],
                timestamp=tilt_data['timestamp'],
            )),
        }
        _webhook = webhook.Webhook(config=_config)
        _webhook.emit()

    # <start config sample>
    # [influxdb]
    # url = www.foo.com
    # port = 80
    # database = tilty
    # gravity_payload_template = {"measurement": "gravity", "tags": {"color": "{{ color }}"}, "fields": {"value": {{ gravity }}}}  # noqa  # pylint: disable=line-too-long
    # temperature_payload_template = {"measurement": "temperature", "tags": {"color": "{{ color }}"}, "fields": {"value": {{ temp }}}}  # noqa  # pylint: disable=line-too-long
    if config.has_section('influxdb'):
        _gravity_template = Template(config['influxdb']['gravity_payload_template'])  # noqa
        _temperature_template = Template(config['influxdb']['temperature_payload_template'])  # noqa
        _config = {
            'url': config['influxdb']['url'],
            'database': config['influxdb']['database'],
            'temperature_payload': _temperature_template.render(
                color=tilt_data['color'],
                gravity=tilt_data['gravity'],
                temp=tilt_data['temp'],
                timestamp=tilt_data['timestamp'],
            ),
            'gravity_payload': _gravity_template.render(
                color=tilt_data['color'],
                gravity=tilt_data['gravity'],
                temp=tilt_data['temp'],
                timestamp=tilt_data['timestamp'],
            ),
        }
        _influxdb = influxdb.InfluxDB(config=_config)
        _influxdb.emit()

    # <start config sample>
    # [datadog]
    # host = 'host'
    # port = 'port'
    if config.has_section('datadog'):
        _config = {
            'host': config['datadog']['host'],
            'port': config['datadog']['port'],
            'gravity': tilt_data['gravity'],
            'temperature': tilt_data['temp'],
            'color': tilt_data['color'],
        }
        _datadog = datadog.Datadog(config=_config)
        _datadog.emit()
