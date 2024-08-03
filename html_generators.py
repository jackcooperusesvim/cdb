import pandas as pd
from icecream import ic
from queries import CoopDb
import config

def generate_header(data:pd.DataFrame) -> str:
    out = "<tr>"
    for col_name in data.columns:
        out+= "<th>"+col_name+"</th>"

    out +="</tr>"
    return out

def edit_button(id: int):
    return f'<td><button hx-target="#record{str(id)}" hx-headers=\'{{"id": "{str(id)}"}}\' hx-get="/edit_child">{str(id)}</button></td>'

def family_to_option(data: pd.DataFrame):
    return f'''<option value="{data.id}-{data.last_name}">{data.id}-{data.last_name}</option>'''

def class_to_option(data: pd.DataFrame):
    return f'''<option value="{data.id}-{data.name}">{data.id}-{data.name}</option>'''
def GRADE_OPTIONS():
    out = ""
    for name in config.GRADE_NAMES():
        out += f'''<option value="{name}">{name}</option>'''
    return out



def child_edit_form(id: int):
    db = CoopDb("test.db")
    data = db.disp_child(id)
    fam = db.read_table("families")

    classnames = db.read_table("classes").id
    children = db.disp_children()

    date = data[data['id'] == data.id]

    ic(type(data))
    ic(data)
    ic(data.id)

    return f'''<form id="form{data.id[0]}">
    <label for="first_name">First Name:</label><br>
    <input type="text" id="first_name" value="{str(data.first_name.iloc[0])}"><br>

    <label for="birthday">Birthday:</label><br>
    <input type="date" id="birthday" name="birthday" value="{data.birthday.iloc[0]}"><br>

    <label for="first_id">Class One:</label><br>
    <select name=text" id="first_id">
    {"/n".join(list(classnames.apply(class_to_option,axis=1)))}
    </select><br>

    <label for="second_id">Class Two:</label><br>
    <select name=text" id="second_id">
    {"/n".join(list(classnames.apply(class_to_option,axis=1)))}
    </select><br>

    <label for="parent">Parent:</label><br>
    <select name=text" id="parent">
    {"/n".join(list(fam.apply(family_to_option,axis=1)))}
    </select><br>

    <label for="grade">Grade:</label><br>
    <select name=text" id="grade" value={str(data.grade.iloc[0])}>
    {GRADE_OPTIONS()}
    </select><br>

    <label for="reset">Reset</label><br>
    <button id="reset" hx-get="/form_edit_child" hx-swap="outerHTML" hx-target="#form{id}">Reset</button><br>

    <label for="cancel">Cancel</label><br>
    <button id="cancel" hx-swap="delete" hx-target="#form{id}">Cancel</button><br>

    <label for="submit">Submit</label><br>
    <input type="submit" id="submit" hx-swap="delete" hx-target="#form{id}"><br>

    </form>'''

def family_edit_form(id: int):
    pass

def class_edit_form(id: int):
    pass

def blank_row(data: pd.DataFrame):
    out = f'''<div id = 'record{data.id.iloc[0]}'
    hx-swap="afterbegin" hx-trigger="load" hx-get="/form_edit_child" hx-target="#forms"></div>'''
    return out

def html_table_records(data: pd.DataFrame):
    out = ""
    for _, record in data.iterrows():
        id = record.id
        record_str = f'<tr hx-headers=\'{{"id": "{str(id)}"}}\' id=record{str(id)}>'
        for field in record:
            record_str+= "<td>"+str(field)+"</td>"

        out+= record_str+edit_button(id)+"</tr>"

        id+=1
    return out
 
def html_table(data: pd.DataFrame) -> str:

    out = "<table border=1>"+generate_header(data)
    out += html_table_records(data)
    out += "</table>"

    return out

def child_record(data: pd.DataFrame):
    assert data.shape == (1,9)
