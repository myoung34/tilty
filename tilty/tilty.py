# -*- coding: utf-8 -*-
""" Class to encapsulate all the emitter logic """
import logging
import sys

from tilty.exceptions import ConfigurationFileEmptyException

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
LOGGER.addHandler(handler)


def parse_config(config):
    """ Parse the config

    config (dict): configuration file loaded from disk
    """
    emitters = []
    if not config.sections():
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
        _config = {}
        for config_key, config_val in config[emitter].items():
            _config.setdefault(config_key, config_val)

        emitters.append(
            getattr(_emitter, _emitter.__type__())(config=_config)
        )

    return emitters


def emit(emitters, tilt_data):
    """ Find and call emitters from config

    general_config (dict): general section from the configuration file
                           loaded from disk
    emitters (obj[]): dynamically loaded emitters from parse_config()
    tilt_data (dict): data returned from valid tilt device scan
    """
    for emitter in emitters:
        emitter.emit(tilt_data=tilt_data)
