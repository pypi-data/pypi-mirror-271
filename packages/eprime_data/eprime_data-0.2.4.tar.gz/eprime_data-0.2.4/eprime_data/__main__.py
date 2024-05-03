"""
Command line interface for EPrima-data
"""

import argparse
import sys
from pathlib import Path
from typing import List

from . import __version__, __author__
from .lib import EPrimeLogFile


def cli():
    parser = argparse.ArgumentParser(
        description="E-Prima-data {}: Converting E-Prime log-data (.txt)".format(
            __version__),
        epilog=f"(c) {__author__}")

    parser.add_argument("FILES", nargs='+', default=None,
                        help="E-prime data file(s) or glob pattern. Single or multiple file names or a string representing a glob pattern that matches multiple files to be processed")

    parser.add_argument("--csv", dest="csv",
                        action="store_true",
                        help="convert to csv",
                        default=False)

    parser.add_argument("--feather", dest="feather",
                        action="store_true",
                        help="convert to feather",
                        default=False)

    parser.add_argument('-l', '--level', type=int, default=-1,
                        help="data level to extract")

    parser.add_argument('--override',  dest="override",
                        action="store_true",
                        help="override existing files (only used if processing multiple files)")

    # parser.add_argument("--stdout", dest="stdout", # TODO
    #                    action="store_true",
    #                    help="print to stdout",
    #                    default=False)

    args = vars(parser.parse_args())

    if args["FILES"] is None:
        print("Please specify a source file or glob pattern (with *) of sources files")
        print("Use -h for help")
        sys.exit()

    data_files: List[Path] = []
    for flname in args["FILES"]:
        if flname.find("*") >= 0:
            # glob file pattern
            data_files.extend(Path().glob(flname))
        else:
            data_files.append(Path(flname))

    if len(data_files) == 1:
        args["override"] = True

    for flname in data_files:
        _process_file(flname, csv=args["csv"], feather=args["feather"],
                      level=args["level"], override=args["override"])


def _process_file(dat_file: Path, csv: bool, feather: bool, level: int,
                  override: bool):
    if not dat_file.is_file():
        print(f"Can't open {dat_file}")
        exit()

    dat = EPrimeLogFile(dat_file)
    if not (csv or feather):
        print(EPrimeLogFile(dat_file).info())
        return
    # convert
    exist_levels = sorted(dat.levels.keys())
    if level not in exist_levels:
        print(
            f"Please specify data level to extract. The following levels exists: {exist_levels}")
        exit()

    if csv:
        dest = dat.filename.with_suffix(".csv")
        if override or not dest.is_file():
            dat.to_csv(dest, level=level, add_subject_id=True)
            print(f" converted to csv: {dest}")

    if feather:
        from .dataframe import save_to_feather
        dest = dat_file.with_suffix(".feather")
        if override or not dest.is_file():
            dat.to_csv(dest, level=level, add_subject_id=True)
            save_to_feather(dat, dest, level=level, add_subject_id=True)
            print(f" converted to feather: {dest}")


if __name__ == "__main__":
    cli()
