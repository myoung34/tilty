# -*- coding: utf-8 -*-
""" SQLite emitter """
import logging
import sqlite3

LOGGER = logging.getLogger()


class SQLite:  # pylint: disable=too-few-public-methods
    """ SQLite wrapper class """

    def __init__(self, config):
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        self.color = config['color']
        self.gravity = config['gravity']
        self.temp = config['temp']
        self.mac = config['mac']
        self.conn = sqlite3.connect(config['file'])
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS data(
              id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
              gravity INTEGER,
              temp INTEGER,
              color VARCHAR(16),
              mac VARCHAR(17),
              timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)
        ''')

    def emit(self, **kwargs):  # pylint: disable=no-self-use,unused-argument
        """ Initializer

        Args:
        """
        LOGGER.info('[sqlite] creating row')
        self.conn.execute(
            "insert into data (gravity,temp,color,mac) values (?,?,?,?)",
            (self.gravity, self.temp, self.color, self.mac)
        )
