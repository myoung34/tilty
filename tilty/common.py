# -*- coding: utf-8 -*-
""" Common methods """

from typing import Any, Optional


def safe_get_key(config: dict, key: str, fallback: Optional[Any] = None):
    """ Class to safely pull key from config or a fallback value

    Args:
        config (dict): The configuration (dict) to try and pull from
        key (str): The config key to try and get.
        fallback (TODO): TODO
    """
    try:
        return config[key]
    except KeyError:
        pass
    return fallback
