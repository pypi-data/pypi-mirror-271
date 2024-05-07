import os

from lhc.misc.argparse import main_with_tools


if __name__ == '__main__':
    import sys
    sys.exit(main_with_tools(
        os.path.dirname(__file__),
        'lhc.cli.alignments',
        description='Tools for working with read alignments.',
    ))
