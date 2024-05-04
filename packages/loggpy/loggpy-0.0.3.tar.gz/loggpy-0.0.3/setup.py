# -*- coding: utf-8 -*-
import io
import re
from setuptools import setup


with io.open("loggpy/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)


setup(
    name='loggpy',
    version=version,
    packages=['loggpy'],
    description="Custom log levels for Python's logging module.",
    url='https://github.com/ReiDoBrega/loggpy',
    keywords=['logging', 'logger', 'verbose'],
    license='MIT'
)
