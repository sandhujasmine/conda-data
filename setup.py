'''
'''

from setuptools import setup, find_packages

import versioneer


setup(
    name='conda_data',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Sean Ross-Ross',
    author_email='sean.ross-ross@continuum.io',
    url='',
    description='Conda data package',
    packages=find_packages(),
    install_requires=['binstar'],
    entry_points={
          'console_scripts': [
              'conda-data = conda_data.cli:main',
              ]
                 },

)
