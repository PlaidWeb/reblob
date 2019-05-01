""" reblob CLI """

import argparse
import logging

from . import convert, __version__

LOG_LEVELS = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]


def parse_args(*args):
    """ Parse the arguments for the command """
    parser = argparse.ArgumentParser(
        description="Quote and link to a webpage in a Markdown entry",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', action='version',
                        version="%(prog)s " + __version__.__version__)
    parser.add_argument("-v", action="count",
                        help="increase output verbosity",
                        default=0)

    parser.add_argument('url', type=str, nargs='+',
                        help="The original page URLs")

    parser.add_argument('--format', '-f', type=str,
                        help='''
Output format; see https://pandoc.org/MANUAL.html#option--to
for available options''',
                        default='gfm')

    return parser.parse_args(*args)


def main():
    """ entry point """
    args = parse_args()
    logging.basicConfig(level=LOG_LEVELS[min(
        args.v, len(LOG_LEVELS) - 1)])

    for url in args.url:
        print(convert(url, output_format=args.format))


if __name__ == '__main__':
    main()
