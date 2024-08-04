import lorem
from icecream import ic
import names
from random import randint
from queries import *
from geonamescache import GeonamesCache
import datetime

# TESTING VARIABLES
NUM_FAMILIES = 10
NUM_CHILDREN = 15
NUM_CLASSES = 5

PERM_NUM_FAMILIES = 200
PERM_NUM_CHILDREN = 300
PERM_NUM_CLASSES = 15

def generate_random_family():
    mnName = names.get_first_name(gender = "female")
    secName = names.get_first_name(gender = "male")
    lName = names.get_last_name()

    # All the roads and cities will have anthropromorphic names because its easier
    rName = str(randint(1,100))+" "+names.get_last_name()+ " Rd."
    cName = names.get_last_name()+"town"

    gc = GeonamesCache()
    state = list(gc.get_us_states().keys())[randint(0,50)]


    zip = randint(1,99999)
    phone1 = randint(1,9999999999)
    phone2 = randint(1,9999999999)
    phone3 = None
    if randint(0,1) == 1:
        phone3 = randint(1,9999999999)

    email_options = ["gmail.com","outlook.office.com","proton.me","yahoo.com"]

    email = lName+"@"+email_options[randint(0,3)]
    membership = randint(0,1) == 1

    Note = None
    if randint(0,10) == 10:
        Note = lorem.get_sentence()


    return mnName, secName, lName, rName, cName, state, zip, phone1, phone2, phone3,email,membership, Note

def generate_random_child(parent_indices: list[int],class_indices: list[int]):
    fName = names.get_first_name()
    birthday = datetime.date(year = randint(2006,2023),month = randint(1,12), day = randint(1,28))
    return (fName, 
        birthday, 
        parent_indices[randint(0,len(parent_indices)-1)],
        class_indices[randint(0,len(class_indices)-1)], 
        parent_indices[randint(0,len(class_indices)-1)], 
        0)

def generate_random_class():
    classname = f'''{lorem.get_word()}-{randint(1,3)}0{randint(1,2)}'''

    desc = ""
    if randint(0,2) == 0:
        desc = lorem.get_sentence()

    secName = names.get_first_name(gender = "male")
    lName = names.get_last_name()

    regular_cost = randint(150,200)
    member_cost = 0
    if randint(0,5) == 0:
        member_cost = randint(40,100)
    hour = randint(1,2)
    return classname, desc, hour, member_cost, regular_cost


def generate_testing_db(location = ":memory:") -> CoopDb:
    cdb = CoopDb(location)
    cdb.create_tables()
    parent_indices = []
    class_indices = []
    for i in range(NUM_FAMILIES):
        parent_indices.append(cdb.add_family(*generate_random_family()))
    for i in range(NUM_CLASSES):
        try:
            class_indices.append(cdb.add_class(*generate_random_class()))
        except sqlite3.IntegrityError:
            ic("integrity-error")
    for i in range(NUM_CHILDREN):
        cdb.add_child(*generate_random_child(parent_indices,class_indices))
    return cdb

def generate_perm_testing_db(location = "test.db"):
    cdb = CoopDb(location)
    cdb.create_tables()
    parent_indices = []
    class_indices = []
    for i in range(PERM_NUM_FAMILIES):
        parent_indices.append(cdb.add_family(*generate_random_family()))
    for i in range(PERM_NUM_CLASSES):
        try:
            class_indices.append(cdb.add_class(*generate_random_class()))
        except sqlite3.IntegrityError:
            ic("integrity-error")
    for i in range(PERM_NUM_CHILDREN):
        cdb.add_child(*generate_random_child(parent_indices,class_indices))
    cdb.commit()
    return cdb


if __name__ == "__main__":
    tdb = generate_testing_db()
    ic(tdb.read_table("children"))
    ic(tdb.read_table("families"))
