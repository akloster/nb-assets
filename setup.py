#!/usr/bin/env python

from distutils.core import setup

setup(name='nb-assets',
      version='0.1',
      description='Asset management for IPython notebook.',
      author='Andreas Klostermann',
      author_email='andreas.klostermann@gmail.com',
      packages=['nb_assets'],
      install_requires=['pygments']
     )


