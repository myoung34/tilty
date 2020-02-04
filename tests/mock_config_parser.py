# -*- coding: utf-8 -*-
class MockConfigParser:
    def __init__(self):
        pass

    def __getitem__(self, key):
        return {
            'url': 'http://www.google.com',
            'headers': {'Content-Type': 'application/json'},
            'payload_template': '{"color": "{{ color }}", "gravity": {{ gravity }}, "temp": {{ temp }}, "timestamp": "{{ timestamp }}"}',
            'method': 'GET'
        }

    def has_section(*args, **kwargs):
        return True
