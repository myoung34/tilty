# -*- coding: utf-8 -*-
from unittest import mock

from tilty.emitters import sqlite


@mock.patch('tilty.emitters.sqlite.sqlite3')
def test_sqlite(
    mock_sqlite_client,
):
    config = {
        'file': '/etc/tilty/tilt.sqlite',
        'color': 'black',
        'mac': '00:0a:95:9d:68:16',
        'gravity': 1000,
        'temp': 80,
    }
    sqlite.SQLite(config=config).emit()
    assert mock_sqlite_client.mock_calls == [
        mock.call.connect('/etc/tilty/tilt.sqlite'),
        mock.call.connect().execute('\n            CREATE TABLE IF NOT EXISTS data(\n              id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\n              gravity INTEGER,\n              temp INTEGER,\n              color VARCHAR(16),\n              mac VARCHAR(17),\n              timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)\n        '),  # noqa
        mock.call.connect().execute('insert into data (gravity,temp,color,mac) values (?,?,?,?)', (1000, 80, 'black', '00:0a:95:9d:68:16'))  # noqa
    ]
