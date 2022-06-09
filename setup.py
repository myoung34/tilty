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
        'click==7.1.2',
        'datadog==0.34.1',
        'influxdb-client==1.17.0',
        'jinja2==3.0.1',
        'prometheus-client==0.8.0',
        'pybluez==0.22',
        'requests==2.25.1',
        'urllib3>=1.26.5',
        'google-auth==1.30.1',
        'google-api-core==1.20.1',
        'google-api-python-client==1.11.0',
        'google-auth-httplib2==0.0.4',
        'google-auth-oauthlib==0.4.4',
        'oauth2client==4.1.3',
        'protobuf==3.17.2',
    ],
    entry_points={
        'console_scripts': [
            'tilty=tilty.cli:run',
        ],
    },
)
