# -*- coding: utf-8 -*-
""" Class to encapsulate all the emitter logic """
import configparser
import logging
from typing import Any, List

from tilty.exceptions import ConfigurationFileEmptyException

LOGGER = logging.getLogger()


def parse_config(config: configparser.ConfigParser) -> List[dict]:
    """ Parse the config

    Args:
        config (dict): configuration file loaded from disk
    """
    emitters = []
    if not [section for section in config.sections() if section != 'general']:
        raise ConfigurationFileEmptyException
    for emitter in config.sections():
        if emitter == 'general':
            continue
        LOGGER.info(
            "Loading emitter: %s (%s)",
            emitter,
            f"{__name__.rsplit('.')[0]}.emitters.{emitter}"
        )
        _emitter = __import__(
            f"{__name__.rsplit('.')[0]}.emitters.{emitter}",
            fromlist=['']
        )
        _config: dict = {}
        for config_key, config_val in config[emitter].items():
            _config.setdefault(config_key, config_val)

        emitters.append(
            getattr(_emitter, _emitter.__type__())(config=_config)
        )

    return emitters


def emit(emitters: List[Any], tilt_data: dict) -> None:
    """ Find and call emitters from config

    Args:
        general_config (dict): general section from the configuration file
                               loaded from disk
        emitters (obj[]): dynamically loaded emitters from parse_config()
        tilt_data (dict): data returned from valid tilt device scan
    """
    for emitter in emitters:
        emitter.emit(tilt_data=tilt_data)
