# -*- coding: utf-8 -*-
""" Custom Exceptions """


class ConfigurationFileNotFoundException(Exception):
    """ Raised when the configuration file is not found """


class ConfigurationFileEmptyException(Exception):
    """ Raised when the configuration file is completely empty """
