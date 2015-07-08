'''
    conda data upload ./data

'''
from __future__ import unicode_literals, print_function

import argparse
import logging

import conda_data


log = logging.getLogger('conda-data.sync')


CHUNK_SIZE = 2 ** 13

def main(args):

    filename = conda_data.pull(args.source)

    log.info('Synced: %s' % args.source)
    log.info('Filename: %s' % filename)


def add_parser(subparsers):
    description = 'Sync packages from anaconda.org'
    parser = subparsers.add_parser('pull',
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   help=description, description=description,
                                   epilog=__doc__)

    parser.add_argument('source', help='Data to sync')
    parser.set_defaults(main=main, no_progress=False)
