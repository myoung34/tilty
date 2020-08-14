# -*- coding: utf-8 -*-
from tilty.emitters import stdout


def test_stdout_type(
):
    assert stdout.__type__() == 'Stdout'


def test_stdout():
    config = {}
    stdout.Stdout(config=config).emit(tilt_data={
        'color': 'black',
        'mac': '00:0a:95:9d:68:16',
        'gravity': 1000,
        'temp': 80,
    })
