import config
from datetime import datetime
import gradedates
from typing import Any

from html_generators import error_message
import html_generators as htmlg

class ValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)

def validate_form(table: str, form_data: dict[str,str]) -> dict[str,Any]:
    out_dict = dict()
    match table:
        case "families":
            city = form_data["city"]

            is_member: bool
            if form_data["is_member"] == "False":
                is_member =  False
            elif form_data["is_member"]  == "True":
                is_member = True
            elif bool(int(form_data["is_member"])):
                is_member = True
            elif not bool(int(form_data["is_member"])):
                is_member = False
            else:
                raise ValidationException(f"membership status is neither True nor False but is {form_data["is_member"]}")

            email: str = form_data["email"]
            v = validate_email(email)
            email = v["email"]

            last_name: str = form_data["last_name"]
            note: str = form_data["note"]
            parent_mn: str = form_data["parent_mn"]
            parent_sec: str = form_data["parent_sec"]

            try:
                phone1: int = int(form_data["phone1"])
                assert (phone1 >= 1000000000) and (phone1 <= 9999999999)

            except AssertionError:
                raise ValidationException(f"phone1 ({form_data["phone1"]}) is not a valid phone number (int between and including 1000000000 and 9999999999)")

            try:
                phone2: int = int(form_data["phone2"])
                assert (phone2 >= 1000000000) and (phone2 <= 9999999999)
            except AssertionError:
                raise ValidationException(f"phone2 ({form_data["phone2"]}) is not a valid phone number (int between and including 1000000000 and 9999999999)")

            phone3: int | None = None
            try:
                if form_data["phone3"]!= "null" and form_data["phone3"]!= "":
                    phone3: int | None = int(form_data["phone3"])
                    assert (phone3 >= 1000000000) and (phone3 <= 9999999999)
            except AssertionError:
                raise ValidationException(f"phone3 ({form_data["phone3"]}) is neither a valid phone number (int between and including 1000000000 and 9999999999) nor \"null\" ")

            
            state: str = form_data["state"]
            state = state.upper()
            if len(state)!=2:
                raise ValidationException(f"state must a valid two-letter state code")

            street: str = form_data["street"]

            zip_str = form_data["zip"]
            try:
                zip: int | None = int(form_data["zip"])
                assert zip >= 0 and zip <= 99999
                assert len(zip_str) == 5
            except AssertionError:
                raise ValidationException(f"\n\nzip ({form_data["zip"]}) is neither a valid zip code (int between and including 0 and 99999 with ) nor \"null\" ")

            out_dict["parent_mn"]  = parent_mn
            out_dict["parent_sec"]  = parent_sec
            out_dict["last_name"]  = last_name
            out_dict["street"]  = street
            out_dict["city"]  = city
            out_dict["state"]  = state
            out_dict["zip"]  = zip
            out_dict["phone1"]  = phone1
            out_dict["phone2"]  = phone2
            out_dict["phone3"]  = phone3
            out_dict["email"]  = email
            if is_member:
                out_dict["is_member"]  = 'True' 
            else:
                out_dict["is_member"]  = 'False'
            out_dict["note"]  = note

            return out_dict

        case "children":

            out_dict["first_name"] = form_data["first_name"]
            out_dict["birthday"] = gradedates.str_to_dt(form_data["birthday"])
            out_dict["first_id"] = int(form_data["first_id"])
            out_dict["second_id"] = int(form_data["second_id"])
            out_dict["family_id"] = int(form_data["family_id"])
            out_dict["grade_offset"] = str(gradedates.from_grade(out_dict["birthday"], form_data["grade"]))
            out_dict["birthday"] = str(form_data["birthday"])

            return out_dict

        case 'first_hour' | 'second_hour':

            out_dict["class_name"] = form_data["class_name"]
            out_dict["desc"] = form_data["desc"]
            out_dict["member_cost"] = int(float(form_data["member_cost"])*100)/100
            out_dict["regular_cost"] = int(float(form_data["regular_cost"])*100)/100
            return out_dict
        case _:
            raise ValidationException(f"table name is neither children nor families nor first_hour nor second_hour but {table}")

def reconstruct_form(table: str, form_data: dict[str,str]) -> str:
    id = -1
    err = ''
    try:
        validate_form(table,form_data)
    except Exception as e:
        err = error_message(str(e))
    out_dict = dict()
    match table:
        case "families":
            return f'''<form id="form{id}">
                {err}
                    <input type="number" name ="id" id="id" value="{id}" hidden><br>

                    <label for="parent_mn">Main Parent:</label><br>
                    <input type="text" name="parent_mn" id="parent_mn" value="{out_dict['parent_mn']}"><br>

                    <label for="parent_sec">Secondary Parent:</label><br>
                    <input type="text" name="parent_sec" id="parent_sec" value="{out_dict['parent_sec']}"><br>

                    <label for="last_name">Last Name:</label><br>
                    <input type="text" name="last_name" id="last_name" value="{out_dict['last_name']}"><br>

                    <label for="street">Street:</label><br>
                    <input type="text" name="street" id="street" value="{out_dict['street']}"><br>

                    <label for="city">City:</label><br>
                    <input type="text" name="city" id="city" value="{out_dict['city']}"><br>

                    <label for="state">State:</label><br>
                    <input type="text" name="state" id="state" value="{out_dict['state']}"><br>

                    <label for="zip">Zip:</label><br>
                    <input type="text" name="zip" pattern="[0-9]{{6}}" id="zip" value="{out_dict['zip']}"><br>

                    <label for="phone1">Primary Phone:</label><br>
                    <input type="tel" name="phone1" pattern="[0-9]{{10}}" id="phone1" value="{out_dict['phone1']}"><br>

                    <label for="phone2">Secondary Phone:</label><br>
                    <input type="tel" name="phone2" id="phone2" pattern="[0-9]{{10}}" value="{out_dict['phone2']}"><br>

                    <label for="phone3">Tertiary Phone:</label><br>
                    <input type="tel" name="phone3" id="phone3" pattern="[0-9]{{10}}" value="{out_dict['phone3']}"><br>

                    <label for="email">Email:</label><br>
                    <input type="email" name="email" id="email" value="{out_dict['email']}"><br>

                    <label for="is_member">Is Member:</label><br>
                    <select id="is_member" name="is_member">
                        {is_member_options(is_member)}
                    </select><br>
                    
                    <label for="note">Note:</label><br>
                    <input type="text" name="note" id="note" value="{out_dict['note']}"><br>

                {form_buttons(id,table)}
                    </form>'''

        case "children":
            connection = new_conn()

            if err != '':
                err = error_message(err)

            grades = list(config.GRADE_NAMES())

            families = connection.execute('SELECT CONCAT(last_name, \'|\', id) AS family FROM families ORDER BY family').fetchall()
            first_hour = connection.execute('SELECT CONCAT(class_name,\'|\', id) AS class FROM first_hour ORDER BY class;').fetchall()
            second_hour = connection.execute('SELECT CONCAT(class_name,\'|\', id) AS class FROM second_hour ORDER BY class;').fetchall()

            families = [family[0] for family in families]
            first_hour = [c[0] for c in first_hour] 
            second_hour = [c[0] for c in second_hour]

            adj_grades = list_to_options(grades,"")

            grade, first_name,family,class_one, class_two, birthday, grade_offset = '','','','','',str(datetime.datetime.today().date),0
            grade_section = adj_grades
            auto_calc_grades = ["Auto Calc"]
            auto_calc_grades = list_to_options(auto_calc_grades,auto_calc_grades[0])
            grade_section = f'''
            <optgroup label="Auto Calc">
            {auto_calc_grades}
            </optgroup>
            <optgroup label="Manual Offset">
            {adj_grades}
            </optgroup>'''

            families = htmlg.list_to_options(families,family)
            first_hour = htmlg.list_to_options(first_hour,class_one)
            second_hour = htmlg.list_to_options(second_hour,class_two)

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
            {grade_section}
            </select><br>

            <br>

            {form_buttons(id,table)}
           <br>
            </form>'''



            return out_dict

        case 'first_hour' | 'second_hour':
            return f'''<form id="form{id}">
            {err}
                <input type="number" name="id" id="id" value="{id}" hidden><br>

                <label for="class_name">Class Name:</label><br>
                <input type="text" name="class_name" id="class_name" value="{out_dict['class_name']}"><br>

                <label for="desc">Description:</label><br>
                <input type="text" name="desc" id="desc" value="{out_dict['desc']}"><br>

                <label for="member_cost">Member Cost:</label><br>
                <input type="text" name="member_cost" id="member_cost" value="{out_dict['member_cost']}"><br>

                <label for="regular_cost">Regular Cost:</label><br>
                <input type="number" name="regular_cost" id="regular_cost" value="{out_dict['regular_cost']}"><br>
            {form_buttons(id,table)}
           </form>'''

        case _:
            raise ValidationException(f"table name is neither children nor families nor first_hour nor second_hour but {table}")

