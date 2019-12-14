"""Setup file for the package"""
from setuptools import find_packages, setup

setup(
    name='Tilty',
    description='A pluggable system to receive and transmit bluetooth events from the Tilt Hydrometer', # noqa
    author='Marcus Young',
    author_email='3vilpenguin@gmail.com',
    py_modules=['tilty', 'blescan'],
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'Click',
        'pybluez',
    ],
    entry_points={
        'console_scripts': [
            'tilty=tilty.cli:run',
        ],
    },
)
