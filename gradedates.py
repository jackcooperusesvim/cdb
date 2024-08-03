import datetime
from icecream import ic
import config


def END_DATE(offset: int = 0) -> datetime.date:
    # The spreadsheet used 9/1/{end of the current coop year} as a marker for classifying grade
    return datetime.date(year=YEAR_OF_COOP()-offset,month=config.START_MONTH(),day=config.START_DAY())

def YEAR_OF_COOP() -> int:
    today = datetime.date.today()

    if today.month<config.START_MONTH():
        return today.year
    else:
        return today.year+1

def GRADE_LENGTH()-> list[int]:
    return [4,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

def GRADE_DICT() -> dict[str, tuple[datetime.date,datetime.date]]:
    '''Gives the starting and ending birthday for every grade in the co-op'''
    out = dict()
    i = 0

    assert len(config.GRADE_NAMES()) == len(GRADE_LENGTH())

    total_offset = 0
    while i<len(config.GRADE_NAMES()):
        relative_offset = GRADE_LENGTH()[i]
        start_date = END_DATE(offset = total_offset+relative_offset)

        end_date = start_date + datetime.timedelta(days = 365*relative_offset)

        start_date += datetime.timedelta(days=1)

        out[config.GRADE_NAMES()[i]] = (start_date, end_date)

        total_offset += relative_offset
        i+=1

    return out

class G():
    DICT = GRADE_DICT()

