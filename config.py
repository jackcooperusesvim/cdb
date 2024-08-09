def DATABASE_FILEPATH() -> str: 
    return "test.db"

def VALID_OPERATIONS():
    return ["add","edit","get_data"]

def VALID_TABLES():
    return ["children","classes","families","first_hour","second_hour"]

def START_MONTH() -> int:
    return 9

def START_DAY() -> int:
    return 1

def GRADE_NAMES() -> list[str]:
    return ["Nursery","Pre-K 1","Pre-K 2","1st","2nd","3rd","4th","5th","6th","7th","8th","9th","10th","11th","12th","Grad"]

def CERTIFY_OP_AND_TABLE(op: str, table: str):
    if not op in VALID_OPERATIONS():
        raise Exception(f"'{op}' is not a valid operation")
    if not table in VALID_TABLES():
        raise Exception(f"'{table}' is not a valid table")

def ARGS_DICT() -> dict[str,list[str]]:
    return {
        "children": [
            "first_name",
             "birthday",
             "family_id",
             "first_id",
             "second_id",
             "grade_offset"],
        "families": [
            "parent_mn",
            "parent_sec",
            "last_name",
            "street",
            "city",
            "state",
            "zip",
            "phone1",
            "phone2",
            "phone3",
            "email",
            "is_member",
            "note"],

        "first_hour": [
            "class_name",
            "desc",
            "member_cost",
            "regular_cost"],

        "second_hour": [
            "class_name",
            "desc",
            "member_cost",
            "regular_cost"],
    }

def AVAILABLE_ARGS(op: str, table: str): 
    CERTIFY_OP_AND_TABLE(op,table)

    #NOTE: SPECIAL RULES HERE:
    if op in ["get_data"] and table == "children":
        return [
            "first_name",
             "family_id",
             "first_hour",
             "second_hour",
             "birthday",
             "grade_offset"]

    return ARGS_DICT()[table]
