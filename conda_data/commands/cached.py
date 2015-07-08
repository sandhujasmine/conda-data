'''
    conda data upload ./data

'''
from __future__ import unicode_literals, print_function

import argparse
import logging

import conda_data
from conda_data.utils import hr_size


log = logging.getLogger('conda-data.sync')


def main(args):

    for item in conda_data.items():
        name = '%(owner)s/%(package)s==%(version)s' % item
        print('%-50s' % name[:50], '%-10s' % hr_size(item['size']), item['summary'])


def add_parser(subparsers):
    description = 'Remove packages from local cache!'
    parser = subparsers.add_parser('cached',
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   help=description, description=description,
                                   epilog=__doc__)

    parser.set_defaults(main=main, no_progress=False)
