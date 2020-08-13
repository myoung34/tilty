# -*- coding: utf-8 -*-
""" SQLite emitter """
import logging
import sqlite3

LOGGER = logging.getLogger()


def __type__() -> str:
    return 'SQLite'


class SQLite:  # pylint: disable=too-few-public-methods
    """ SQLite wrapper class """

    def __init__(self, config: dict) -> None:
        """ Initializer

        Args:
            config: (dict) represents the configuration for the emitter
        """
        # <start config sample>
        # [sqlite]
        # file = /etc/tilty/tilt.sqlite
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

    def emit(self, tilt_data: dict) -> None:
        """ Initializer

        Args:
            tilt_data (dict): data returned from valid tilt device scan
        """
        LOGGER.info('[sqlite] creating row')
        self.conn.execute(
            "insert into data (gravity,temp,color,mac) values (?,?,?,?)",
            (
                tilt_data['gravity'],
                tilt_data['temp'],
                tilt_data['color'],
                tilt_data['mac']
            )
        )
        self.conn.commit()
