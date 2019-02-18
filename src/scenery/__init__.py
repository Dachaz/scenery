import sys
from .Options import getOptions
from .Scenery import Scenery


def main(argv=None):
    try:
        Scenery(getOptions(sys.argv[1:])).run()
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')


__all__ = ['main']
