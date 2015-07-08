'''

    conda data upload data

'''
from __future__ import unicode_literals

import argparse
import logging
import os
from os.path import exists
import time

from binstar_client import errors
from binstar_client.utils import get_binstar, upload_print_callback
from conda_data.utils import ensure_package, ensure_version, ensure_unique, \
    file_or_value

# Python 3 Support
try:
    input = raw_input
except NameError:
    input = input


log = logging.getLogger('conda-data.upload')



def main(args):

    binstar = get_binstar(args)

    print("main upload!")

    if args.dest and '/' in args.dest:
        username = args.dest.split('/', 1)[0]
    else:
        user = binstar.user()
        username = user['login']

    if args.dest:
        package_name = args.dest.rsplit('/', 1)[-1]
    else:
        package_name = os.path.basename(args.datafile).split('.')[0]

    if not exists(args.datafile):
        raise errors.BinstarError('file %s does not exist' % args.datafile)
    package_type = 'data'

    ensure_package(binstar, username, package_name, args.summary)
    ensure_version(binstar, username, package_name, args.version)
    ensure_unique(binstar, username, package_name, args.version, os.path.basename(args.datafile), force=False)

    with open(args.datafile) as fd:
        upload_info = binstar.upload(username, package_name, args.version, os.path.basename(args.datafile),
                                     fd, package_type,
                                     args.description,
                                     attrs={'data_type': 'download'},
                                     channels=['main'],
                                     callback=upload_print_callback(args))

    log.info("\n\nUpload(s) Complete\n")

    package_url = upload_info.get('url', 'https://anaconda.org/%s/%s' % (username, package_name))
    log.info("Package located at:\n%s\n" % package_url)


def add_parser(subparsers):
    description = 'Upload packages to anaconda.org'
    parser = subparsers.add_parser('upload',
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   help=description, description=description,
                                   epilog=__doc__)

    parser.add_argument('datafile', help='Data files to upload')
    parser.add_argument('--dest', help='Anaconda.org destination to store the data (e.g username/package)')
    parser.add_argument('--version', default=time.strftime('%Y.%m.%d+%H%M'),
                        help='version of the data (default: %(default)s)')
    parser.add_argument('--summary',
                        help='Summary description of the data')
    parser.add_argument('--description', type=file_or_value,
                        help='Long description of the data')

    parser.set_defaults(main=main, no_progress=False)
