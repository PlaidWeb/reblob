import argparse
from . import convert, __version__


def parse_args(*args):
    """ Parse the arguments for the command """
    parser = argparse.ArgumentParser(
        description="Quote and link to a webpage in a Markdown entry")
    parser.add_argument('--version', action='version',
                        version="%(prog)s " + __version__.__version__)

    parser.add_argument('url', type=str, nargs='+',
                        help="The original page URLs")
    parser.add_argument('--format', '-f', type=str,
                        help='Output format', default='markdown_github')

    return parser.parse_args(*args)


def main():
    args = parse_args()

    for url in args.url:
        print(convert(url))
