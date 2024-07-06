import pandas as pd
from icecream import ic
from enum import StrEnum,auto

def table(data: pd.DataFrame, child_or_fam: bool) -> str:
    pass
def record_entry(record: dict) -> str:
    pass

def generate_header(data:pd.DataFrame) -> str:
    out = "<tr>"
    for col_name in data.columns:
        out+= "<th>"+col_name+"</th>"

    out +="</tr>"
    return out
def edit_button(id: int):
    return "<td><button>"+str(id)+"</button></td>"

def html_table(data: pd.DataFrame) -> str:

    out = "<table>"+generate_header(data)


    id = 0
    for _, record in data.iterrows():
        record_str = "<tr id = record"+str(id)+">"
        ic(record)
        ic(type(record))
        for field in record:
            record_str+= "<td>"+str(field)+"</td>"
        out+= record_str+edit_button(id)+"</tr>"

        id+=1
    out+="</table>"
    return out

def child_record(data: pd.DataFrame):
    assert data.shape == (1,9)

class childEnum(StrEnum):
    first_name = "first_name"
    birth_year = "birth_year"
fields = ["first_name","birth_year","birth_month","birth_day","family_id","first_id","grade_offset"]
