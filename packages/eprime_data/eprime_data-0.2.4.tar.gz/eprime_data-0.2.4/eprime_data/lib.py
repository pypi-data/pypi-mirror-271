import csv
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from .constants import EPRIME_FILE_ENCODING, RE
from .dict_tab_data import DictTabularData

## TODO ignores currently header data

class EPrimeLogFile(object):
    """Handles e-prime txt data files"""

    def __init__(self, filename: str | Path,
                 replace_dots_in_variable_names: bool = True) -> None:
        self.filename = Path(filename)
        # all data, dict with level tabular data
        self.levels: Dict[int, DictTabularData] = {}
        self.experiment = ""
        self.subject_id = -1
        self.datetime_str = ""
        self._varnames_without_dots = replace_dots_in_variable_names
        self._read_file()

    def data(self, level: int, add_subject_id=True) -> OrderedDict:
        """converts level data (list of dicts) to a
        dict of lists"""

        rtn = OrderedDict()
        if add_subject_id:
            rtn["subject_id"] = [self.subject_id] * self.levels[level].nrow
        rtn.update(self.levels[level].dict)
        return rtn

    def datetime(self) -> Optional[datetime]:
        try:
            return datetime.strptime(self.datetime_str, "%d-%m-%Y %H:%M:%S")
        except AttributeError:
            return None

    def _read_file(self):
        self.levels = {}
        row = OrderedDict()  # current dict
        lvl = 0
        with open(self.filename, "r", encoding=EPRIME_FILE_ENCODING) as fl:
            for l in fl:
                l = l.strip()
                if lvl == 0:
                    new_level = RE.level.match(l)
                    if new_level:
                        lvl = int(new_level.group(1))
                        if lvl not in self.levels:
                            self.levels[lvl] = DictTabularData()
                else:
                    if lvl == 1:
                        experiment = RE.experiment.match(l)
                        if experiment:
                            self.experiment = experiment.group(1)
                        subject = RE.subject.match(l)
                        if subject:
                            self.subject_id = int(subject.group(1))
                        dt = RE.datetime.match(l)
                        if dt:
                            self.datetime_str = dt.group(1)
                    if RE.frame_end.search(l):
                        self.levels[lvl].append(row)
                        lvl = 0
                        row = OrderedDict()
                    elif RE.frame_start.search(l):
                        row = OrderedDict()
                    else:
                        try:
                            key, value = RE.split_variable.split(l.strip())
                        except (KeyError, ValueError):
                            key, value = None, None
                        if key is not None and value is not None:
                            try:
                                v = int(value)
                            except ValueError:
                                try:
                                    v = float(value)
                                except ValueError:
                                    v = value

                            if self._varnames_without_dots:
                                key = key.replace(".", "_")
                            row[key] = v
        return None

    def to_csv(self, file_path: Path | str,
               level: int,
               add_subject_id=False):
        """writes data to a csv file"""
        fieldnames = self.levels[level].names
        if add_subject_id:
            fieldnames = ["subject_id"] + fieldnames
            consts = {"subject_id": self.subject_id}
        else:
            consts = None

        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.levels[level].row_dicts(add_constants=consts):
                writer.writerow(row)

    def info(self, levels:bool=True) -> str:
        rtn = f"## {self.filename} {self.datetime_str}"
        if levels:
            for lvl in sorted(self.levels.keys()):
                rtn += f"\nLevel {lvl}: "
                for cnt, name in enumerate(self.levels[lvl].names):
                    rtn += f"{name}, "
                    if cnt % 4 == 3:
                        rtn += "\n" + " "*9
        return rtn.strip()
