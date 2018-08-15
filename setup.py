#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name='vortex',
    version='0.1',
    description='aiohttp wrapped web framework',
    author='Chris Lee',
    author_email='sihrc.c.lee@gmail.com',
    packages=find_packages(),
    install_requires=open(
        os.path.join(
            os.path.dirname(__file__),
            "requirements.txt"
        ),
        'r'
    ).readlines(),
    extras_require={
        "testing": ["pytest"]
    }
)
