__author__="mscholl"
__date__ ="$Mar 13, 2014 1:49:04 PM$"

from setuptools import setup,find_packages

setup (
  name = 'icmm',
  version = '0.1',
  packages = find_packages(),

  # Declare your packages' dependencies here, for eg:
  install_requires=['foo>=3'],

  # Fill in these to make your Egg ready for upload to
  # PyPI
  author = 'mscholl',
  author_email = 'martin.scholl@cismet.de',

  summary = 'helpers and tools to use the CRISMA ICMM service',
  url = 'https://github.com/crismaproject/icmm_py',
  license = 'LGPLv3',
  long_description= 'Helpers and tools for use with the CRISMA ICMM service',

  # could also include long_description, download_url, classifiers, etc.

  
)