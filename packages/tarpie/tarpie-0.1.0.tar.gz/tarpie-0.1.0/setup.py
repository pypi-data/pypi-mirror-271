import sys
from setuptools import setup

if sys.version_info < (2, 7):
    raise NotImplementedError("Sorry, you need at least Python 2.7 or Python 3.6+ to use bottle.")

import tarpie

setup(name='tarpie',
      version=tarpie.__version__,
      description='The Faster, Smarter pip.',
      author=tarpie.__author__,
      author_email='rayan.m.haddad@proton.me',
      py_modules=['tarpie'],
      scripts=['tarpie.py'],
      license='MIT',
      platforms='any',
      classifiers=['Development Status :: 4 - Beta',
                   "Operating System :: OS Independent",
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   ],
      )