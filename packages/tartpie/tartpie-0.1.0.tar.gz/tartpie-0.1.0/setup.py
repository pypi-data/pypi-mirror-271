import sys
from setuptools import setup

if sys.version_info < (2, 7):
    raise NotImplementedError("Sorry, you need at least Python 2.7 or Python 3.6+ to use bottle.")

import tartpie

setup(name='tartpie',
      version=tartpie.__version__,
      description='Superset of The pip Package Manager.',
      long_description="tartpie",
      long_description_content_type="text/markdown",
      author=tartpie.__author__,
      author_email='rayan.m.haddad@proton.me',
      py_modules=['tartpie'],
      scripts=['tartpie.py'],
      license='MIT',
      platforms='any',
      classifiers=['Development Status :: 4 - Beta',
                   "Operating System :: OS Independent",
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   ],
      )