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
    return [4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

def GRADE_DICT() -> dict[str, tuple[datetime.date]]:
    '''Gives the ending birthday for every grade in the co-op'''
    out = dict()
    i = 0

    assert len(config.GRADE_NAMES()) == len(GRADE_LENGTH())

    total_offset = 0
    while i<len(config.GRADE_NAMES()):
        end_date = END_DATE(offset= total_offset)
        start_date = END_DATE(offset= total_offset+GRADE_LENGTH()[i])+datetime.timedelta(days=1)

        out[config.GRADE_NAMES()[i]] = (start_date,end_date)

        total_offset+=GRADE_LENGTH()[i]
        i+=1

    ic(out["Grad"])
    out["Grad"] =(datetime.date(year=1,month=1,day=1),out["Grad"][1])
    return out

class G():
    DICT = GRADE_DICT()

