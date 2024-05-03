# E-Prime-Data

Python library &amp; command line interface to handle and convert txt-data files from E-prime

(c) Oliver Lindemann

## Install

```
pip install eprime_data
```

## Command line interface

```
usage: __main__.py [-h] [--csv] [--feather] [-l LEVEL] [--override] FILES [FILES ...]

E-Prima-data: Converting E-Prime log-data (.txt)

positional arguments:
  FILES                 E-prime data file(s) or glob pattern. Single or multiple file names or a
                        string representing a glob pattern that matches multiple files to be
                        processed

options:
  -h, --help            show this help message and exit
  --csv                 convert to csv
  --feather             convert to feather
  -l LEVEL, --level LEVEL
                        data level to be extracted
  --override            override existing files (only used if processing multiple files)
```