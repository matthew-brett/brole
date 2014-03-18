#!/usr/bin/env python

from distutils.core import setup

setup(name='brole',
      version='0.1',
      description='sphinx role for including notebooks',
      author='Matthew Brett, Min Ragan-Kelley',
      author_email='matthew.brett@gmail.com',
      url='http://github.com/matthew-brett/brole',
      packages=['brole'],
      package_data={'brole': ['static/{0}/*'.format(sdir)
                              for sdir in ('css', 'js', 'fonts')]},
     )
