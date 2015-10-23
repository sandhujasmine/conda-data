from __future__ import print_function, unicode_literals

from glob import glob
import json
import os
import sys

from odo import odo

from binstar_client.utils import dirs
from binstar_client.utils import get_binstar
from conda_data.utils import md5_file
from conda_data.utils import semantic_version_key
import pandas as pd


# use versioneer to auto generate version number 
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

CHUNK_SIZE = 2 ** 14


from .pull import pull

def get(source=None):

    if source is None:
        info_glob = os.path.join(dirs.user_data_dir, 'conda-data', 'info', '*.json')
    elif '/' in source:
        source = source.lower()
        info_glob = os.path.join(dirs.user_data_dir, 'conda-data', 'info', '%s+%s+*.json' % tuple(source.split('/', 1)))
    else:
        source = source.lower()
        info_glob = os.path.join(dirs.user_data_dir, 'conda-data', 'info', '*+%s+*.json' % source)

    return glob(info_glob)

def items():
    for info_file in get():
        with open(info_file) as fd:
            yield json.load(fd)


def clear(source):
    for info_file in get(source):
        with open(info_file) as fd:
            info = json.load(fd)

        assert 'cache_file' in info, info_file
        if os.path.isfile(info['cache_file']):
            os.unlink(info['cache_file'])
        os.unlink(info_file)
        yield info

