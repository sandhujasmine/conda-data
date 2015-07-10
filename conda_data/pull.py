from __future__ import print_function, unicode_literals

from argparse import Namespace
import json
import os
import sys

from odo import odo

from binstar_client.utils import dirs
from binstar_client.utils import get_binstar
from conda_data.utils import md5_file
from conda_data.utils import semantic_version_key
import pandas as pd


__version__ = '0.0.0'

CHUNK_SIZE = 2 ** 14

def print_callback(n, total):

    if n < total:
        print('.', end=''); sys.stdout.flush()
    else:
        print('.')


def pull(source, target_type='filename', callback=print_callback):

    args = Namespace(site=None, token=None)
    binstar = get_binstar(args)

    if '/' in source:
        username = source.split('/', 1)[0]
    else:
        user = binstar.user()
        username = user['login']

    package_name = source.rsplit('/', 1)[-1]

    pkg = binstar.package(username, package_name)


    file_data = max(pkg['files'], key=semantic_version_key)

    req = binstar.download(username, package_name, file_data['version'], file_data['basename'])

    filename = '+'.join([username, package_name, file_data['version'], file_data['basename']])
    filename = filename.lower()
    cache_file = os.path.join(dirs.user_data_dir, 'conda-data', filename)


    callback(0, 0)
    info_file = os.path.join(dirs.user_data_dir, 'conda-data', 'info', filename.rsplit('.', 1)[0] + '.json')
    if os.path.isfile(cache_file):
        md5 = md5_file(cache_file)
        if file_data['md5'] == md5:
            if target_type == 'filename':
                return cache_file
            return odo(cache_file.encode(), pd.DataFrame)

    if not os.path.exists(os.path.dirname(cache_file)):
        os.makedirs(os.path.dirname(cache_file))

    n = 0
    with open(cache_file, 'wb') as fd:
        data = req.raw.read(CHUNK_SIZE)
        n += len(data)
        while data:
            fd.write(data)
            data = req.raw.read(CHUNK_SIZE)
            n += len(data)
            callback(n, file_data['size'])

        callback(file_data['size'], file_data['size'])
    if not os.path.exists(os.path.dirname(info_file)):
        os.makedirs(os.path.dirname(info_file))

    with open(info_file, 'w') as fd:
        file_data['summary'] = pkg['summary']
        file_data['package'] = pkg['name']
        file_data['cache_file'] = cache_file
        json.dump(file_data, fd)

    if target_type == 'filename':
        return cache_file
    return odo(cache_file.encode(), target_type)

