import lorem
from icecream import ic
import names
from random import randint
from queries import *
from geonamescache import GeonamesCache
import datetime
import sqlite3

# TESTING VARIABLES
NUM_FAMILIES = 10
NUM_CHILDREN = 15
NUM_CLASSES = 5

PERM_NUM_FAMILIES = 200
PERM_NUM_CHILDREN = 300
PERM_NUM_CLASSES = 15

def generate_random_family(connection: sqlite3.Connection) -> int:
    out = dict()
    out["parent_mn"]= names.get_first_name(gender = "female")
    out["parent_sec"]= names.get_first_name(gender = "male")
    out["last_name"]= names.get_last_name()

    # All the roads and cities will have anthropromorphic names because its easier
    out["street"] = str(randint(1,100))+" "+names.get_last_name()+ " Rd."
    out["city"] = names.get_last_name()+"town"

    gc = GeonamesCache()
    out["state"] = list(gc.get_us_states().keys())[randint(0,50)]


    out["zip"]= randint(1,99999)
    out["phone1"] = randint(1,9999999999)
    out["phone2"] = randint(1,9999999999)
    out["phone3"] = "null"
    if randint(0,1) == 1:
        out["phone3"] = randint(1,9999999999)

    email_options = ["gmail.com","outlook.office.com","proton.me","yahoo.com"]

    out["email"] = out['last_name']+"@"+email_options[randint(0,3)]
    out["is_member"] = randint(0,1) == 1

    if randint(0,10) == 10:
        out["note"] = lorem.get_sentence()

    for key in out:
        out[key] = str(out[key])

    return db_action(connection,"add","families", input_options = out)
    

def generate_random_child(connection: sqlite3.Connection,
                          parent_indices: list[int],
                          first_hour_indices: list[int], 
                          second_hour_indices: list[int]) ->int:
    out = dict()
    out["first_name"]= names.get_first_name()
    out["birthday"] = datetime.date(year = randint(2006,2023),month = randint(1,12), day = randint(1,28))
    out["family_id"] = parent_indices[randint(0,len(parent_indices)-1)]
    out["first_id"] = first_hour_indices[randint(0,len(first_hour_indices)-1)]
    out["second_id"] = second_hour_indices[randint(0,len(second_hour_indices)-1)]
    out["grade_offset"] = randint(-1,1)
    for key in out:
        out[key] = str(out[key])

    return db_action(connection,"add","children", input_options = out)

def generate_random_class(connection: sqlite3.Connection, table: str):
    out = dict()
    out["class_name"]= f'''{lorem.get_word()}-{randint(1,3)}0{randint(1,2)}'''

    out["desc"] = "null"
    if randint(0,2) == 0:
        out["desc"] = lorem.get_sentence()


    out["regular_cost"] = randint(150,200)
    out["member_cost"] = 0
    if randint(0,5) == 0:
        out["member_cost"] = randint(40,100)

    for key in out:
        out[key] = str(out[key])

    return db_action(connection,"add", table, input_options = out)


def generate_testing_db():
    init_db()
    connection = new_conn()
    parent_indices = []
    first_hour_indices = []
    second_hour_indices = []
    for i in range(PERM_NUM_FAMILIES):
        parent_indices.append(generate_random_family(connection))

    for i in range(PERM_NUM_CLASSES):
        try:
            second_hour_indices.append(generate_random_class(connection,"second_hour"))
        except sqlite3.IntegrityError as e:
            ic(e)
    for i in range(PERM_NUM_CLASSES):
        try:
            first_hour_indices.append(generate_random_class(connection,"first_hour"))
        except sqlite3.IntegrityError as e:
            ic(e)


    for i in range(PERM_NUM_CHILDREN):
        generate_random_child(connection,parent_indices,first_hour_indices,second_hour_indices)

    connection.commit()

if __name__ == "__main__":
    generate_testing_db()
    con = new_conn()
    ic(db_action(con,"get_data","first_hour"))
    ic(db_action(con,"get_data","children"))
    ic(db_action(con,"get_data","families"))
    ic(db_action(con,"get_data","second_hour"))
