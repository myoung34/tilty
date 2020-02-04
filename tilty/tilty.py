# -*- coding: utf-8 -*-
""" Class to encapsulate all the emitter logic """
import json

from jinja2 import Template

from tilty.emitters import webhook


def emit(config, tilt_data):
    """ Find and call emitters from config

    config (dict): configuration file loaded from disk
    tilt_data (dict): data returned from valid tilt device scan
    """
    if tilt_data is None:
        return

    if config.has_section('webhook'):
        _template = Template(config['webhook']['payload_template'])
        _config = {
            'url': config['webhook']['url'],
            'headers': config['webhook'].get('headers'),
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
