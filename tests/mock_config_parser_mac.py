# -*- coding: utf-8 -*-
class MockConfigParserMac:
    def __init__(self, section):
        self.section = section

    def __getitem__(self, key):
        if self.section == 'webhook':
            return {
                'url': 'http://www.google.com',
                'headers': '{"Content-Type": "application/json"}',
                'payload_template': '{"color": "{{ color }}", "gravity": {{ gravity }}, "temp": {{ temp }}, "mac": "{{ mac }}", "timestamp": "{{ timestamp }}"}',  # noqa
                'method': 'GET'
            }
        if self.section == 'influxdb':
            return {
                'url': 'http://www.google.com',
                'database': 'foo',
                'gravity_payload_template': 'gravity,mac={{ mac }} color={{ color }} value={{ gravity }} {{timestamp}}',  # noqa
                'temperature_payload_template': 'temperature,scale=fahrenheit,mac={{ mac }} color={{ color }} value={{ temp }} {{timestamp}}',  # noqa
            }
        if self.section == 'datadog':
            return {
                'host': 'http://api.datadog.com',
                'port': '8120',
            }
        return None

    def has_section(self, *args, **kwargs):
        return self.section in args
