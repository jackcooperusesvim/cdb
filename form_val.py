from flask import request
from datetime import datetime
import gradedates
from email_validator import validate_email, EmailNotValidError
from typing import Any

class ValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)

def validate_form(table: str, form_data: dict[str,str]) -> dict[str,Any]:
    out_dict = dict()
    if table == "families":
        city = form_data["city"]

        is_member: bool
        if form_data["is_member"] == "False":
            is_member =  False
        elif form_data["is_member"]  == "True":
            is_member = True
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
            if form_data["phone3"]!= "null":
                phone3: int | None = int(form_data["phone3"])
                assert (phone3 >= 1000000000) and (phone3 <= 9999999999)
        except AssertionError:
            raise ValidationException(f"phone3 ({form_data["phone3"]}) is neither a valid phone number (int between and including 1000000000 and 9999999999) nor \"null\" ")

        
        state: str = form_data["state"]
        state = state.upper()
        if len(state)!=2:
            raise ValidationException(f"state must a valid two-letter state code")

        street: str = form_data["street"]

        try:
            zip: int | None = int(form_data["zip"])
            assert zip >= 10000 and zip <= 99999
        except AssertionError:
            raise ValidationException(f"\n\nzip ({form_data["zip"]}) is neither a valid zip code (int between and including 1000000 and 999999) nor \"null\" ")

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
        out_dict["is_member"]  = is_member
        out_dict["note"]  = note

        return out_dict

    elif table == "children":

        out_dict["first_name"] = form_data["first_name"]
        out_dict["birthday"] = gradedates.str_to_dt(form_data["birthday"])
        out_dict["first_id"] = int(form_data["first_id"])
        out_dict["second_id"] = int(form_data["second_id"])
        out_dict["family_id"] = int(form_data["family_id"])
        out_dict["grade_offset"] = str(gradedates.from_grade(out_dict["birthday"], form_data["grade"]))
        out_dict["birthday"] = str(form_data["birthday"])

        return out_dict
    elif table in ['first_hour','second_hour']:
        out_dict["class_name"] = form_data["class_name"]
        out_dict["desc"] = form_data["desc"]
        out_dict["member_cost"] = int(float(form_data["member_cost"])*100)/100
        out_dict["regular_cost"] = int(float(form_data["regular_cost"])*100)/100
        return out_dict
    else:
        raise ValidationException(f"table name is neither children nor families nor first_hour nor second_hour but {table}")

    return {}
