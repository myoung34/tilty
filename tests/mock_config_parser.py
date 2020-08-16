# -*- coding: utf-8 -*-
class MockConfigParser:
    def __init__(
        self,
        section,
        return_empty=False,
        include_extra_section=False,
        include_invalid_section=False,
    ):
        self.section = section
        self.include_extra_section = include_extra_section
        self.return_empty = return_empty
        self.include_invalid_section = include_invalid_section

    def __getitem__(self, key):
        if self.section == 'google':
            return {
                "client_id": "1111111111",
                "client_secret": "222222222",
                "spreadsheet_id": "333333333333",
                "refresh_token": "5555555555555555",
            }
        if self.section == 'sqlite':
            return {
                'file': '/foo.sqlite',
            }
        if self.section == 'webhook':
            return {
                'url': 'http://www.google.com',
                'headers': '{"Content-Type": "application/json"}',
                'payload_template': '{"color": "{{ color }}", "gravity": {{ gravity }}, "temp": {{ temp }}, "timestamp": "{{ timestamp }}"}',  # noqa
                'method': 'GET'
            }
        if self.section == 'influxdb':
            return {
                'url': 'http://www.google.com',
                'database': 'foo',
                'gravity_payload_template': 'gravity,color={{ color }} value={{ gravity }} {{timestamp}}',  # noqa
                'temperature_payload_template': 'temperature,scale=fahrenheit,color={{ color }} value={{ temp }} {{timestamp}}',  # noqa
            }
        if self.section == 'datadog':
            return {
                'host': 'http://api.datadog.com',
                'port': '8120',
            }
        return {}

    def sections(self, *args, **kwargs):
        if self.include_extra_section:
            return ['general', self.section]
        if self.include_invalid_section:
            return ['general', 'fake']
        if self.return_empty:
            return []
        return ['general']

    def has_section(self, *args, **kwargs):
        return self.section in args
