# -*- coding: utf-8 -*-
""" Common methods """


def safe_get_key(config, key, fallback=None):
    """ Class to safely pull key from config or a fallback value """
    try:
        return config[key]
    except KeyError:
        pass
    return fallback
