from collections import OrderedDict
from typing import Dict, Optional

class DictTabularData(object):
    """It's basically a dict of lists that ensures that all columns have the same
    amount of elements"""

    NaN = None

    def __init__(self) -> None:
        self.dict: Dict[str, list] = OrderedDict()
        self.nrow: int = 0

    @property
    def ncol(self) -> int:
        """number of columns"""
        return len(self.dict)

    @property
    def names(self) -> list:
        """column names"""
        return list(self.dict.keys())

    def row_dicts(self, add_constants: Optional[dict] = None) -> list:
        """list of dicts with data in each row
        """
        rtn = []
        for i in range(self.nrow):
            if isinstance(add_constants, dict):
                row_dict = OrderedDict(add_constants)
            else:
                row_dict = OrderedDict()
            row_dict.update({k: v[i] for k, v in self.dict.items()})
            rtn.append(row_dict)
        return rtn

    def append(self, data: dict):
        """append a row of data
        """
        common = set(self.dict.keys()).intersection(data.keys())
        #  add values for existing columns
        for k, lst in self.dict.items():
            if k in common:
                lst.append(data[k])
            else:
                # missing column
                lst.append(DictTabularData.NaN)

        # add new columns
        for k in data.keys():
            if k not in common:
                # new column
                self.dict[k] = [DictTabularData.NaN] * self.nrow
                self.dict[k].append(data[k])

        self.nrow += 1
