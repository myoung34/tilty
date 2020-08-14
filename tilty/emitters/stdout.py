# -*- coding: utf-8 -*-
""" stdout emitter """
import logging

LOGGER = logging.getLogger()


def __type__() -> str:
    return 'Stdout'


class Stdout:  # pylint: disable=too-few-public-methods
    """ Stdout wrapper class """

    def __init__(self, config: dict) -> None:
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        # <start config sample>
        # [stdout]

    def emit(self, tilt_data: dict) -> None:
        """ Initializer

        Args:
            tilt_data (dict): data returned from valid tilt device scan
        """
