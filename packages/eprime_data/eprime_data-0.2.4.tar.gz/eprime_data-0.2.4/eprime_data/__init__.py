"""Library & command line interface to handle and convert txt-data files from E-prime"""

__version__ = "0.2.4"
__author__ = "Oliver Lindemann"

import sys as _sys
from .lib import EPrimeLogFile


if _sys.version_info[0] != 3 or _sys.version_info[1] < 10:

    raise RuntimeError("{} {} ".format("EPrime-data", __version__) +
                        "is not compatible with Python {0}.{1}.".format(
        _sys.version_info[0],
        _sys.version_info[1]) +
        "\n\nPlease use Python 3.10 or higher.")


