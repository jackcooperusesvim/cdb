import pandas as pd
from icecream import ic
from queries import new_conn, db_action
import queries
import config
import gradedates
import datetime

def generate_header(data:pd.DataFrame) -> str:
    out = "<tr>"
    for col_name in data.columns:
        out+= "<th>"+col_name+"</th>"

    out +="</tr>"
    return out

def error_message(message:str):
    return f'<h4>{message}</h4><br>'

def edit_button(id: int,table: str):
    return f'<td><button onclick="top_scroll()" hx-swap="outerHTML" hx-target="#record{str(id)}" {headers(id,table)}  hx-get="/form_loader">{str(id)}</button></td>'

def list_to_options(in_list: list[str], current_option: str):
    out = ""
    for idstr in in_list:
        id = idstr
        if '|' in idstr:
            id = idstr.split('|')[1]
        if idstr == current_option:
           out += f'''<option selected="selected" value="{id}">{idstr}</option>\n'''
        else:
            out += f'''<option value="{id}">{idstr}</option>\n'''
    return out

def child_edit_form(id: int, err:str = ''):
    connection = new_conn()

    if err != '':
        err = error_message(err)

    q = queries.get_query("get_data","children")
    q = q[:len(q)-2]+f" WHERE children.id = {id};"


    grades = list(config.GRADE_NAMES())

    _, first_name,family,class_one, class_two, birthday, grade_offset = connection.execute(q).fetchall()[0]

    grade = gradedates.to_grade(gradedates.str_to_dt(birthday),grade_offset)

    families = connection.execute('SELECT CONCAT(last_name, \'|\', id) AS family FROM families ORDER BY family').fetchall()

    first_hour = connection.execute('SELECT CONCAT(class_name,\'|\', id) AS class FROM first_hour ORDER BY class;').fetchall()

    second_hour = connection.execute('SELECT CONCAT(class_name,\'|\', id) AS class FROM second_hour ORDER BY class;').fetchall()

    families = [family[0] for family in families]
    first_hour = [c[0] for c in first_hour] 
    second_hour = [c[0] for c in second_hour]
    auto_calc_grades = [f"Keep Offset|{grade}",f"Remove Offset|{gradedates.to_grade(birthday,0)}"]

    families = list_to_options(families,family)
    first_hour = list_to_options(first_hour,class_one)
    second_hour = list_to_options(second_hour,class_two)

    adj_grades = list_to_options(grades,"")
    auto_calc_grades = list_to_options(auto_calc_grades,auto_calc_grades[0])

    return f'''<form id="form{id}">
    {err}
    <input type="number" id="id" name="id" value="{id}" hidden><br>

    <label for="first_name">First Name:</label><br>
    <input type="text" id="first_name" name="first_name" value="{first_name}"><br>

    <label for="birthday">Birthday:</label><br>
    <input type="date" id="birthday" name="birthday" value="{birthday}"><br>

    <label for="first_id">Class One:</label><br>
    <select name="first_id" id="first_id" name="first_id">
    {first_hour}
    </select><br>

    <label for="second_id">Class Two:</label><br>
    <select name="second_id" id="second_id" name="second_id">
    {second_hour}
    </select><br>

    <label for="family_id">Parent:</label><br>
    <select name="family_id" id="parent" name="parent">
    {families}
    </select><br>

    <label for="grade">Grade:</label><br>
    <select name="grade" id="grade" value={grade} name="grade">
    <optgroup label="Auto Calc">
    {auto_calc_grades}
    </optgroup>
    <optgroup label="Offset Grade">
    {adj_grades}
    </optgroup>
    </select><br>

    <br>

    <button id="cancel" hx-get="/blank_endpoint" hx-swap="delete" hx-target="#form{id}">Cancel</button>

    <br>

    <button id="reset" {headers(id,"children")} hx-get="/form" hx-swap="outerHTML" hx-target="#form{id}">Reset</button><br>
    <br>

    <button id="submit" {headers(id, "children")} hx-post="/submit" hx-swap="delete" hx-target="#form{id}">Submit</button><br>
    <br>
    </form>'''

def is_member_options(is_member: bool) -> str:
    membopts= f'''<option selected="selected" value="{is_member}">{is_member}</option>
    <option value="{not is_member}">{not is_member}</option>'''
    ic(membopts)
    return membopts

def family_edit_form(id: int, err:str = ''):
    if err != '':
        err = error_message(err)
    connection = new_conn()
    id, parent_mn, parent_sec, last_name, street, city, state, zip, phone1, phone2, phone3, email, is_member, note = db_action(connection, "get_data","families", where_id = id)[0]
    if is_member == "False":
        is_member = False
    if is_member == "True":
        is_member = True

    return f'''<form id="form{id}">
    {err}
        <input type="number" name ="id" id="id" value="{id}" hidden><br>

        <label for="parent_mn">Main Parent:</label><br>
        <input type="text" name="parent_mn" id="parent_mn" value="{parent_mn}"><br>

        <label for="parent_sec">Secondary Parent:</label><br>
        <input type="text" name="parent_sec" id="parent_sec" value="{parent_sec}"><br>

        <label for="last_name">Last Name:</label><br>
        <input type="text" name="last_name" id="last_name" value="{last_name}"><br>

        <label for="street">Street:</label><br>
        <input type="text" name="street" id="street" value="{street}"><br>

        <label for="city">City:</label><br>
        <input type="text" name="city" id="city" value="{city}"><br>

        <label for="state">State:</label><br>
        <input type="text" name="state" id="state" value="{state}"><br>

        <label for="zip">Zip:</label><br>
        <input type="text" name="zip" pattern="[0-9]{{6}}" id="zip" value="{zip}"><br>

        <label for="phone1">Primary Phone:</label><br>
        <input type="tel" name="phone1" pattern="[0-9]{{10}}" id="phone1" value="{phone1}"><br>

        <label for="phone2">Secondary Phone:</label><br>
        <input type="tel" name="phone2" id="phone2" pattern="[0-9]{{10}}" value="{phone2}"><br>

        <label for="phone3">Tertiary Phone:</label><br>
        <input type="tel" name="phone3" id="phone3" pattern="[0-9]{{10}}" value="{phone3}"><br>

        <label for="email">Email:</label><br>
        <input type="email" name="email" id="email" value="{email}"><br>

        <label for="is_member">Is Member:</label><br>
        <select id="is_member" name="is_member">
            {is_member_options(is_member)}
        </select><br>
        
        <label for="note">Note:</label><br>
        <input type="text" name="note" id="note" value="{note}"><br>

        <br>

        <button id="cancel" hx-get="/blank_endpoint" hx-swap="delete" hx-target="#form{id}">Cancel</button><br>


        <button id="reset" {headers(id,"families")} hx-get="/form" hx-swap="outerHTML" hx-target="#form{id}">Reset</button><br>
        <br>

        <button id="submit" {headers(id, "families")} hx-post="/submit" hx-swap="outerHTML" hx-target="#form{id}">Submit</button><br>
        <br>
        </form>'''



def class_edit_form(id: int, hour: str, err:str = ''):
    ic(hour)
    connection = new_conn()
    _, class_name, desc, member_cost, regular_cost = db_action(connection, "get_data",hour, where_id = id)[0]
    if err != '':
        err = error_message(err)

    return f'''<form id="form{id}">
    {err}
        <input type="number" name="id" id="id" value="{id}" hidden><br>

        <label for="class_name">Class Name:</label><br>
        <input type="text" name="class_name" id="class_name" value="{class_name}"><br>

        <label for="desc">Description:</label><br>
        <input type="text" name="desc" id="desc" value="{desc}"><br>

        <label for="member_cost">Member Cost:</label><br>
        <input type="text" name="member_cost" id="member_cost" value="{member_cost}"><br>

        <label for="regular_cost">Regular Cost:</label><br>
        <input type="number" name="regular_cost" id="regular_cost" value="{regular_cost}"><br>

        <button id="cancel" hx-get="/blank_endpoint" hx-swap="delete" hx-target="#form{id}">Cancel</button><br>

        <button id="reset" {headers(id,hour)} hx-get="/form" hx-swap="outerHTML" hx-target="#form{id}">Reset</button><br>
        <br>

        <button id="submit" {headers(id,hour)} hx-post="/submit" hx-swap="outerHTML" hx-target="#form{id}">Submit</button><br>
        <br>
        </form>'''



def headers(id: int | None, table: str):
    if id is None:
        return f'''hx-headers=\'{{"table": "{table}"}}\''''
    else:
        return f'''hx-headers=\'{{"id": "{id}", "table": "{table}"}}\''''

def blank_row(data,table):

    id = data["id"]
    if table == "children":
        bday = gradedates.str_to_dt(data["birthday"])
        offset = int(data['grade_offset'])
        data["grade"] = gradedates.to_grade(bday,offset)

    out = f'<tr id=record{id} {headers(id,table)} hx-swap="innerHTML" hx-trigger="load" hx-get="/form" hx-target="#forms">'

    for field in data:
            out += f"<td>{data[field]}</td>"

    out+= edit_button(id,table)+"</tr>"
    ic(out)
    return out

def html_table_records(data: pd.DataFrame,table:str):
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
    ic(data)
    if table == "children":
        data['grade'] = data.apply(gradedates.to_grade_pd,axis=1)
        ic("CHILDREN")
        ic(data)

    out = "<table border=1 class='table'>"+generate_header(data)
    out += html_table_records(data, table)
    out += "</table>"

    return out

