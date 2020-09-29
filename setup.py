#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="vortex-http",
    version="0.4.1",
    description="aiohttp wrapped web framework",
    author="Chris Lee",
    author_email="sihrc.c.lee@gmail.com",
    packages=find_packages(),
    install_requires=[
        "aiodns==2.0.0",
        "aiohttp==3.6.2",
        "cchardet==2.1.6",
        "setuptools==50.0.3",
        "wheel==0.35.1",
    ],
    extras_require={
        "testing": ["pytest", "pytest-aiohttp"],
        "auth": ["PyJWT==1.7.1"],
        "db": ["sqlalchemy==1.3.18"],
    },
)
