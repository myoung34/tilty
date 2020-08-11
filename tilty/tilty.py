# -*- coding: utf-8 -*-
""" Class to encapsulate all the emitter logic """
import logging

LOGGER = logging.getLogger()


def parse_config(config):
    """ Parse the config

    config (dict): configuration file loaded from disk
    """
    emitters = []
    for emitter in config.sections():
        if emitter == 'general':
            continue
        try:
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
                _config.setdefault(config_key, []).append(config_val)

            emitters.append(_emitter(config=_config))

        except ModuleNotFoundError:
            LOGGER.warning("No emitter named 'tilty.emitters.{emitter}'. Skipping and continuing.")  # noqa  #pylint:disable=line-too-long
            continue

    return emitters


def emit(emitters, tilt_data):
    """ Find and call emitters from config

    general_config (dict): general section from the configuration file
                           loaded from disk
    emitters (obj[]): dynamically loaded emitters from parse_config()
    tilt_data (dict): data returned from valid tilt device scan
    """
    if tilt_data is None:
        return

    for emitter in emitters:
        emitter.emit(tilt_data=tilt_data)
