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
    version='0.12.0',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'click>=7.0,<8.0',
        'datadog>=0.34.1,<0.35.0',
        'google-api-core==1.20.1',
        'google-api-python-client>=1.10.0,<2.0.0',
        'google-auth-httplib2>=0.0.4,<0.0.5',
        'google-auth-oauthlib>=0.4.1,<0.5.0',
        'influxdb-client>=1.12.0,<2.0.0',
        'jinja2>=2.11.3',
        'oauth2client>=4.1.3,<5.0.0',
        'prometheus_client>=0.8.0,<0.9.0',
        'pybluez @ git+https://github.com/tonyfettes/pybluez.git@bluez-use-bytes',
        'requests>=2.22,<3.0',
        'urllib3>=1.26.5',
    ],
    entry_points={
        'console_scripts': [
            'tilty=tilty.cli:run',
        ],
    },
)
