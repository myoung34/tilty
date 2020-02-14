# -*- coding: utf-8 -*-
"""Setup file for the package"""
from setuptools import find_packages, setup

setup(
    name='Tilty',
    description='A pluggable system to receive and transmit bluetooth events from the Tilt Hydrometer', # noqa
    author='Marcus Young',
    author_email='3vilpenguin@gmail.com',
    py_modules=['tilty', 'blescan'],
    version='0.2.0',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Click',
        'influxdb',
        'Jinja2',
        'pybluez',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'tilty=tilty.cli:run',
        ],
    },
)
