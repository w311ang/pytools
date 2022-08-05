#!/usr/bin/env python

from distutils.core import setup
import os

with open('version.txt') as f:
  version=f.read().splitlines()[0]

setup(name='MyPytools',
      version=version,
      description='My Python utility',
      author='w311ang',
      author_email='w311angw311ang@gmail.com',
      url='https://github.com/w311ang/pytools',
      packages=['pytools'],
      install_requires=[
        'requests',
        'PyCryptodome',
        'psutil',
        'beautifulsoup4',
        'lxml',
        'dnspython',
        'httpx',
        'pywin32' if os.name == "nt" else ''
      ]
      )
