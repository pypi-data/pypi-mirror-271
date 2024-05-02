# -*- coding: utf-8 -*-

"""
Copyright (C) 2024, Zato Source s.r.o. https://zato.io

Licensed under SSPL 1.0, see LICENSE.txt for terms and conditions.
"""

# stdlib
import os
from setuptools import setup, find_packages

version = '24.1.35'

LONG_DESCRIPTION = """

Write API tests for your [API integrations](https://zato.io) in plain English, with no programming needed.

Here is how it looks like:

<a href="https://zato.io">![API testing in Python](https://upcdn.io/kW15bqq/raw/root/en/docs/3.2/gfx/api-testing/demo.webp)</a>

More information about API testing: https://zato.io/en/docs/3.2/api-testing/index.html

"""

def parse_requirements(requirements): # type: ignore
    ignored = ['#', 'setuptools', '-e']

    with open(requirements) as f:
        return [line for line in f if line.strip() and not any(line.startswith(prefix) for prefix in ignored)]

setup(
      name = 'zato-apitest',
      version = version,

      scripts = ['src/zato/apitest/console/apitest'],

      author = 'Zato Source s.r.o.',
      author_email = 'info@zato.io',
      url = 'https://zato.io',
      description = 'API Testing for Humans. Write API tests in pure English, without any programming needed.',
      long_description = LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      platforms = ['OS Independent'],
      license = 'SSPL 1.0',

      package_dir = {'':'src'},
      packages = find_packages('src'),

      namespace_packages = ['zato'],
      install_requires = parse_requirements(
          os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')),

      zip_safe = False,

      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Education :: Testing',
        'Topic :: Internet',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
        ],
)
