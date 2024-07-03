import datetime
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




def GRADE_DICT() -> dict[str, datetime.date]:
    #TODO: CHECK THIS FUNCTION
    out = dict()
    i = 0

    assert len(config.GRADE_NAMES()) == len(GRADE_LENGTH())

    total_offset = 0
    while i<len(config.GRADE_NAMES()):
        out[config.GRADE_NAMES()[i]] = END_DATE(offset = total_offset+GRADE_LENGTH()[i])
        i+=1

    return out





# TODO: FINISH THIS
def get_student_grade(birth_year: int, 
                      birth_month: int, 
                      birth_day: int,
                      offset: int):
    pass
