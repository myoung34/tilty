# -*- coding: utf-8 -*-
"""Setup file for the package"""
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Tilty',
    description='A pluggable system to receive and transmit bluetooth events from the Tilt Hydrometer', # noqa
    author='Marcus Young',
    author_email='3vilpenguin@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['tilty', 'blescan'],
    version='0.3.1',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Click',
        'datadog',
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
