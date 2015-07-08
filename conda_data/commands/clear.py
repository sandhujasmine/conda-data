'''
    conda data upload ./data

'''
from __future__ import unicode_literals, print_function

import argparse
import logging

import conda_data


log = logging.getLogger('conda-data.sync')


def main(args):

    for cleared in conda_data.clear(args.source):
        print('removed', cleared, 'from cache')


def add_parser(subparsers):
    description = 'Remove packages from local cache!'
    parser = subparsers.add_parser('clear',
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   help=description, description=description,
                                   epilog=__doc__)

    parser.add_argument('source', help='Data to sync')
    parser.set_defaults(main=main, no_progress=False)
