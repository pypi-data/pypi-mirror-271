import re

EPRIME_FILE_ENCODING = 'utf_16_le'

class RE():
    frame_end = re.compile(r"\*\*\* LogFrame End \*\*\*")
    frame_start = re.compile(r"\*\*\* LogFrame Start \*\*\*")
    split_variable = re.compile(r":\s")
    level = re.compile(r"Level:\s(\d+)")
    subject = re.compile(r"Subject:\s(\d+)")
    experiment = re.compile(r"Experiment:\s(\w+)")
    datetime = re.compile(r"SessionStartDateTimeUtc:\s(.+)")

