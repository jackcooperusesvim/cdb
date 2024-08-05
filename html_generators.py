import pandas as pd
from icecream import ic
from queries import CoopDb, new_conn
import config

def generate_header(data:pd.DataFrame) -> str:
    out = "<tr>"
    for col_name in data.columns:
        out+= "<th>"+col_name+"</th>"

    out +="</tr>"
    return out

def form_space():
    return "<div id=forms border=1></div>"
def edit_button(id: int,table: str):
    return f'<td><button hx-swap="outerHTML" hx-target="#record{str(id)}" {headers(id,table)}  hx-get="/form_loader">{str(id)}</button></td>'

def family_to_option(data: pd.DataFrame):
    if data.current_option:
        return f'''<option selected="selected" value="{data.id}-{data.last_name}">{data.id}-{data.last_name}</option>'''
    else:
        return f'''<option value="{data.id}-{data.last_name}">{data.id}-{data.last_name}</option>'''

def class_to_option(data: pd.DataFrame):
    if data.current_option:
        return f'''<option selected="selected" value="{data.id}-{data.class_name}">{data.id}-{data.class_name}</option>'''
    else:
        return f'''<option value="{data.id}-{data.class_name}">{data.id}-{data.class_name}</option>'''

def grade_to_options():
    out = ""
    for name in config.GRADE_NAMES():
        out += f'''<option value="{name}">{name}</option>'''
    return out

def generate_table(data: pd.DataFrame):
    pass

def child_edit_form(id: int):
    connection = new_conn()

    classnames = db.read_table("classes")

    grade_names = config.GRADE_NAMES()
    grade_names["current_option"] = grade_names["grade"] == int(data["grade"].iloc[0])
    grade_options = "\n".join(list(grade_names.apply(grade_to_option,axis=1)))

    ic(data['first_id'].iloc[0])
    ic(classnames["id"])

    ic(classnames.current_option.unique())

    return f'''<form class="form{id}">
    <input type="number" id="id" value="{id}" disabled hidden><br>

    <label for="first_name">First Name:</label><br>
    <input type="text" id="first_name" value="{str(data.first_name.iloc[0])}"><br>

    <label for="birthday">Birthday:</label><br>
    <input type="date" id="birthday" name="birthday" value="{data.birthday.iloc[0]}"><br>

    <label for="first_id">Class One:</label><br>
    <select name="first_id" id="first_id">
    {first_class_options}
    </select><br>

    <label for="second_id">Class Two:</label><br>
    <select name="second_id" id="second_id">
    {second_class_options}
    </select><br>

    <label for="parent">Parent:</label><br>
    <select name=parent" id="parent">
    {family_options}
    </select><br>

    <label for="grade">Grade:</label><br>
    <select name="grade" id="grade" value={data.grade.iloc[0]}>
    {grade_options}
    </select><br>

    <button id="cancel" hx-get="blank_endpoint" hx-swap="delete" hx-target=".form{id}">Cancel</button><br>

    <button id="reset" {headers(id,"children")}hx-get="/form" hx-swap="outerHTML" hx-target=".form{id}">Reset</button><br>

    <button id="submit" {headers(id, "children")} hx-post="/submit_child" hx-swap="delete" hx-target=".form{id}">Submit</button><br>
    </form>'''


def family_edit_form(id: int):
    pass

def class_edit_form(id: int):
    pass

def headers(id: int, table: str):
    return f'''hx-headers=\'{{"id": "{id}", "table": "{table}"}}\''''

def blank_row(data,table):

    id = data["id"]
    out = f'<tr id=record{id} {headers(id,table)} hx-swap="innerHTML" hx-trigger="load" hx-get="/form" hx-target="#forms">'

    for field in data:
            out += f"<td>{data[field]}</td>"

    out+= edit_button(id,table)+"</tr>"
    ic(out)
    return out

def html_table_records(data: pd.DataFrame,table:str):
    ic(data)
    out = ""
    for _, record in data.iterrows():
        id = record.id
        record_str = f'<tr {headers(id,table)} id=record{str(id)}>'
        for field in record:
            record_str+= f"<td>{field}</td>"

        out+= record_str+edit_button(id,table)+"</tr>"

        id+=1
    return out
 
def html_table(data: pd.DataFrame, table: str) -> str:

    out = "<table border=1>"+generate_header(data)
    out += html_table_records(data, table)
    out += "</table>"

    return out

