from pathlib import Path

from .lib import EPrimeLogFile

try:
    import pandas as pd
except ModuleNotFoundError as err:
    raise RuntimeError("To using dataframe function please install Pandas!") from err

def dataframe(eprime_data:EPrimeLogFile,
              level: int, add_subject_id=False):
    """returns Pandas dataframe"""
    return pd.DataFrame(eprime_data.data(level=level, add_subject_id=add_subject_id))


def save_to_feather(eprime_data:EPrimeLogFile,
                    arrow_file: Path | str,
                    level: int,
                    add_subject_id:bool=False,
                    compression: str = "zstd"):

    arrow_file = Path(arrow_file)
    rtn = dataframe(eprime_data, level, add_subject_id=add_subject_id)
    rtn.to_feather(arrow_file, compression=compression)
    return rtn


