import datetime
from icecream import ic
import config
import pandas as pd


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

def GRADE_DICT() -> dict[str, tuple[datetime.date,datetime.date]]:
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

    out["Grad"] =(datetime.date(year=1,month=1,day=1),out["Grad"][1])
    return out

def to_grade(birthday:datetime.date, offset:int) -> str:
    grades = GRADE_DICT()
    if type(birthday) is str:
        birthday = str_to_dt(birthday)

    ind = 0
    for grade in grades:

        if grades[grade][0]<=birthday and grades[grade][1]>=birthday:
            break
        ind += 1

    grades = list(grades)
    if ind+offset>=len(grades):
        return grades[len(grades)-1]
    if ind+offset<=0:
        return grades[0]
    return grades[ind+offset]

def to_grade_pd(data) -> str:
    ic()
    return to_grade(data.birthday, data.grade_offset)


def from_grade(birthday: datetime.date, grade:str) -> int:
    grades = list(GRADE_DICT())
    normal_grade = to_grade(birthday,0)
    return grades.index(normal_grade)-grades.index(grade)

def str_to_dt(date_string: str) -> datetime.date:
    date = datetime.datetime.strptime(date_string,"%Y-%m-%d")
    return date.date()
