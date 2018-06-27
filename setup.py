import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="calc",
    version="0.0.1",
    author="Aliaksandr Bahdanovich",
    author_email="bogdanovich.alex@gmail.com",
    description=("Command-line utility to calc and prints evaluated result"),
    keywords="Command-line utility",
    url="http://packages.python.org/calc",
    packages=['tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Homework",
    ],
)