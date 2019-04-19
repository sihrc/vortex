#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="vortex",
    version="0.1",
    description="aiohttp wrapped web framework",
    author="Chris Lee",
    author_email="sihrc.c.lee@gmail.com",
    packages=find_packages(),
    install_requires=[
        "aiodns==2.0.0",
        "aiohttp==3.5.4",
        "cchardet==2.1.4",
        "setuptools==41.0.0",
        "wheel==0.33.1",
    ],
    extras_require={
        "testing": ["pytest", "pytest-aiohttp"],
        "auth": ["PyJWT==1.7.1"],
    },
)
