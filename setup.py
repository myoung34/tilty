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
    version='0.8.1',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Click',
        'datadog',
        'influxdb',
        'Jinja2',
        'prometheus_client==0.8.0',
        'pybluez',
        'requests',
        'urllib3>1.25.1,<1.26',
        'google-auth==1.20.1',
        'google-api-core==1.20.1',
        'google-api-python-client==1.10.0',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'oauth2client',
    ],
    entry_points={
        'console_scripts': [
            'tilty=tilty.cli:run',
        ],
    },
)
