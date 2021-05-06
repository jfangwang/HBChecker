#!/usr/bin/python3
from setuptools import setup
setup(
    name='hbchecker.py',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'hbchecker=hbchecker:run'
        ]
    }
)
