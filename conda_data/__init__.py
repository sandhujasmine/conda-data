from __future__ import print_function, unicode_literals

from argparse import Namespace
import os

from binstar_client.utils import dirs
from binstar_client.utils import get_binstar
from conda_data.utils import semantic_version_key
import sys
import json
from conda_data.utils import md5_file
from glob import glob

__version__ = '0.0.0'

CHUNK_SIZE = 2 ** 14


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


def pull(source):

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


    info_file = os.path.join(dirs.user_data_dir, 'conda-data', 'info', filename.rsplit('.', 1)[0] + '.json')
    if os.path.isfile(cache_file):
        md5 = md5_file(cache_file)
        if file_data['md5'] == md5:
            return cache_file

    if not os.path.exists(os.path.dirname(cache_file)):
        os.makedirs(os.path.dirname(cache_file))

    with open(cache_file, 'wb') as fd:
        data = req.raw.read(CHUNK_SIZE)
        while data:
            fd.write(data)
            data = req.raw.read(CHUNK_SIZE)
            print('.', end=''); sys.stdout.flush()

        print('.')

    if not os.path.exists(os.path.dirname(info_file)):
        os.makedirs(os.path.dirname(info_file))

    with open(info_file, 'w') as fd:
        file_data['summary'] = pkg['summary']
        file_data['package'] = pkg['name']
        file_data['cache_file'] = cache_file
        json.dump(file_data, fd)

    return cache_file

