import re

from binstar_client import errors
from semantic_version import Version
import os
import hashlib

CHUNK_SIZE = 2 ** 13
PAT = re.compile('^(.*)(\.0(\d))(.*)$')


def ensure_package(binstar, username, package_name, summary=None, license=None):
    """
    """
    try:
        binstar.package(username, package_name)
    except errors.NotFound:
        binstar.add_package(username, package_name, summary, license,
                            public=True)

def ensure_version(binstar, username, package_name, version, description=None):
    """
    """
    try:
        binstar.release(username, package_name, version)
    except errors.NotFound:
        binstar.add_release(username, package_name, version, None, None, description)


def ensure_unique(binstar, username, package_name, version, basename, force):
    try:
        binstar.distribution(username, package_name, version, basename)
        full_name = '%s/%s/%s/%s' % (username, package_name, version, basename)
        raise errors.UserError('File already exists on server. Please use the --force options or `binstar remove %s`' % full_name)
    except errors.NotFound:
        return True




def semantic_version_key(file_data):
    return Version.coerce(make_safe_version(file_data['version']))

def make_safe_version(version, build=None):
    if build and '_' in build:
        build_str, build_no = build.split('_', 1)
        build = '%s.%s' % (build_no, build_str)


    while PAT.match(version):
        version = PAT.sub(r'\1.\3\4', version)

    if version.startswith('.'):
        version = '0' + version

    if not build:
        return version
    else:
        return '%s+%s' % (version, build)



def file_or_value(value):

    if os.path.isfile(value):
        with open(value) as fd:
            return fd.read().strip()
    return value



def hashsum_file(path, mode='md5'):
    h = hashlib.new(mode)
    with open(path, 'rb') as fi:
        while True:
            chunk = fi.read(CHUNK_SIZE)  # process chunks of 256KB
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def md5_file(path):
    return hashsum_file(path, 'md5')



def hr_size(length):
    if not length:
        return 0
    if length < 1024:
        return '%iB' % length
    length /= 1024.
    if length < 1024:
        return '%.1fKB' % round(length, 1)
    length /= 1024.
    if length < 1024:
        return '%.1fMB' % round(length, 1)
    length /= 1024.
    if length < 1024:
        return '%.1fGB' % round(length, 1)

    return length
