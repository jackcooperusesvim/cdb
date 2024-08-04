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
    return f'<td><button hx-swap="outerHTML" hx-target="#record{str(id)}" hx-headers=\'{{"id": "{str(id)}"}}\' hx-get="/edit_child">{str(id)}</button></td>'

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



def child_edit_form(id: int):
    db = CoopDb("test.db")
    data = db.disp_child(id)
    family = db.read_table("families")

    classnames = db.read_table("classes")

    classnames["current_option"] = classnames["id"] == int(data["first_id"].iloc[0])
    first_class_options = "\n".join(list(classnames.apply(class_to_option,axis=1)))

    classnames["current_option"] = classnames["id"] == int(data["second_id"].iloc[0])
    second_class_options = "\n".join(list(classnames.apply(class_to_option,axis=1)))

    family["current_option"] = family["id"] == int(data["family_id"].iloc[0])
    family_options = "\n".join(list(family.apply(family_to_option,axis=1)))

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

    <button id="reset" hx-headers=\'{{"id": "{id}"}}\' hx-get="/form_edit_child" hx-swap="outerHTML" hx-target=".form{id}">Reset</button><br>

    <button id="submit" hx-headers=\'{{"id": "{id}"}}\' hx-post="/submit_child" hx-swap="delete" hx-target=".form{id}">Submit</button><br>
    </form>'''



def family_edit_form(id: int):
    pass

def class_edit_form(id: int):
    pass

def blank_row(data: pd.DataFrame):
    ic(data)

    id = list(data.id)[0]
    out = f'<tr id=record{id} hx-headers=\'{{"id": "{str(id)}"}}\' hx-swap="afterbegin" hx-trigger="load" hx-get="/form_edit_child" hx-target="#forms">'

    for field in data:
            out += f"<td>{list(data[field])[0]}</td>"

    out+= edit_button(id)+"</tr>"
    ic(out)
    return out

def html_table_records(data: pd.DataFrame):
    ic(data)
    out = ""
    for _, record in data.iterrows():
        id = record.id
        record_str = f'<tr hx-headers=\'{{"id": "{str(id)}"}}\' id=record{str(id)}>'
        for field in record:
            record_str+= f"<td>{field}</td>"

        out+= record_str+edit_button(id)+"</tr>"

        id+=1
    return out
 
def html_table(data: pd.DataFrame) -> str:

    out = "<table border=1>"+generate_header(data)
    out += html_table_records(data)
    out += "</table>"

    return out

