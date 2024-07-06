import lorem
from icecream import ic
import names
from random import randint
from queries import *
from geonamescache import GeonamesCache

# TESTING VARIABLES
NUM_FAMILIES = 10
NUM_CHILDREN = 15

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

def generate_random_child(parent_indices: list[int]):
    fName = names.get_first_name()
    birth_year = randint(2006,2023)
    birth_month = randint(1,12)
    birth_day = randint(1,29)
    return fName, birth_year,birth_month, birth_day, parent_indices[randint(0,len(parent_indices)-1)] , None, None, 0


def generate_testing_db(location = ":memory:") -> CoopDb:
    cdb = CoopDb(location)
    cdb.create_tables()
    parent_indices = []
    for i in range(NUM_FAMILIES):
        parent_indices.append(cdb.add_family(*generate_random_family()))
    for i in range(NUM_CHILDREN):
        cdb.add_child(*generate_random_child(parent_indices))
    return cdb

if __name__ == "__main__":
    cdb = CoopDb(":memory:")
    cdb.create_tables()
    parent_indices = []
    for i in range(NUM_FAMILIES):
        parent_indices.append(cdb.add_family(*generate_random_family()))
    for i in range(NUM_CHILDREN):
        cdb.add_child(*generate_random_child(parent_indices))
    ic(cdb.read_table("children"))
    ic(cdb.read_table("families"))
