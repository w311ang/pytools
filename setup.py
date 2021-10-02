#!/usr/bin/env python

from distutils.core import setup

setup(name='MyPytools',
      version='2.1.1',
      description='My Python utility',
      author='w311ang',
      author_email='w311angw311ang@gmail.com',
      url='https://github.com/w311ang/pytools',
      packages=['pytools','_aes'],
      install_requires=[
        'requests',
        'PyCryptodome',
        'psutil'
      ]
      )
