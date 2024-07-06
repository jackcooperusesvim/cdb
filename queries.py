import sqlite3
import html_generators as htmlg
import re
from typing import Any, Callable
from icecream import ic
import config
import pandas as pd
import datetime
from enum import Enum

from gradedates import GRADE_DICT


def exec_query_pandas(connection: sqlite3.Connection,query:str) -> list[pd.DataFrame]:
    results = []
    with open(config.QUERY_DIR()+"/"+query+".sql") as file:
        for query in file.read().split(";"):
            results.append(pd.read_sql_query(query,connection))
    return results

def rc(Str:str,char:str) -> str:
    return " ".join(Str.split(char))

def read_queries(query: str) -> list[str]:
    '''Reads all queries from the .sql file at "config.QUERY_DIR()/{query}.sql"'''
    queries = []
    with open(config.QUERY_DIR()+"/"+query+".sql") as file:
        for query in file.read().split(";"):
            query = rc(rc(query,'\t'),'\n')
            if query != '':
                queries.append(query)
    return queries

class db_field():
    def __init__(self,id: str,t: type, validation: Callable[any,bool] = None):
        self.id = id
        self.type = t
    def __str__(self) -> str:
        return self.id
class children():
    fields = ["first_name","birth_year","birth_month","birth_day","family_id","first_id","grade_offset"]
    first_name = db_field(id = "first_name", t = str)
    birth_year = db_field(id = "birth_year", t = int)
    birth_month = db_field(id = "birth_month", t = int)
    birth_day = db_field(id = "birth_day", t = int)
    family_id = db_field(id = "family_id", t = int)
    first_id = db_field(id = "first_id", t = int)
    grade_offset = db_field(id = "grade_offset", t = int)

class families():
    parent_mn = db_field(id = "parent_mn", t = str)
    parent_sec = db_field(id = "parent_sec", t = str)
    last_name = db_field(id = "last_name", t = str)
    street = db_field(id = "street", t = str)
    city = db_field(id = "city", t = str)
    state = db_field(id = "state", t = str)
    zip = db_field(id = "zip", t = int)
    phone1 = db_field(id = "phone1", t = int)
    phone2 = db_field(id = "phone2", t = int)
    phone3 = db_field(id = "phone3", t = int )
    email = db_field(id = "email", t = str)
    is_member = db_field(id = "is_member", t = Any)
    note = db_field(id = "note", t = Any)

class classes():
    name = db_field(id = "name",t = int)
    desc = "desc"
    hour = "hour"
    member_cost = "member_cost"
    regular_cost = "regular_cost"


class changes():

    def __init__(self, proposed: dict[str,]):
        pass

    def generate_query(self):
        pass


class CoopDb:
    def __init__(self, filepath = config.DATABASE_FILEPATH()+""+config.DEF_DATABASE()):
        self.filepath = filepath
        self.con = sqlite3.connect(filepath)

    def list_tables(self):
        cur = self.con.execute("SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        cur.fetchall()

    def create_tables(self):
        queries = read_queries("init")
        for query in queries:
            self.con.execute(query)

    def commit(self) -> None:
        self.con.commit()

    def read_table(self, table: str):
        return pd.read_sql_query("SELECT * FROM "+table+";",self.con)

    def generate_table_html(self,table_name: str) -> str:
        return htmlg.children_table(self.read_table(table_name))


    def read_grade(self,studentid: int):


        cur = self.con.execute("SELECT birth_day, birth_month, birth_year, grade_offset FROM children WHERE id = ?", (studentid,))

        out = cur.fetchall()[0]

        b_day = out[0]
        b_month = out[1]
        b_year = out[2]
        offset = out[3]

        b_day = datetime.date(b_year,b_month,b_day)+datetime.timedelta(days = 365*offset)

        for name in config.GRADE_NAMES():
            if GRADE_DICT()[name] > b_day:
                return name



        return out


    def find_children(self, fam_id: int):
        query = read_queries("find_children")[0]

        try:
            ic(query)
            cur = self.con.execute(query, (fam_id,)) 
            return cur.fetchall()[0]

        except sqlite3.Error as er:
            ic(er.sqlite_errorcode)
            ic(er.sqlite_errorname)



    # def update_child(self,id: int, changes: dict[str, Any])
    def add_class(self,
                  name: str,
                  desc: str | None,
                  hour: int,
                  member_cost: int,
                  regular_cost: int):
        '''Python wrapper for queries/add_class.sql. Returns a sql error if one occurs'''

        query = read_queries("add_class")[0]

        try:
            cur = self.con.execute(query,(name,desc,hour,member_cost,regular_cost)) 
            return cur.fetchall()[0][0]
        except sqlite3.Error as er:
            ic(er.sqlite_errorcode)
            ic(er.sqlite_errorname)
            raise er



    def add_family(self,
                   parent_mn: str,
                   parent_sec: str,
                   last_name: str,
                   street: str,
                   city: str,
                   state: str,
                   zip: int,
                   phone1: int,
                   phone2: int,
                   phone3: int | None,
                   email: str,
                   is_member: bool,
                   note: str | None) -> int:

        query = read_queries("add_family")[0]
        '''Python wrapper for queries/add_family.sql. Raises a sql error if one occurs and returns the id of the insert'''

        try:
            cur = self.con.execute(query, 
                              (parent_mn,
                               parent_sec,
                               last_name,
                               street,
                               city,
                               state,
                               zip,
                               phone1,
                               phone2,
                               phone3,
                               email,
                               is_member,
                               note))
            return cur.fetchall()[0][0]
        except sqlite3.Error as er:
            ic(er.sqlite_errorcode)
            ic(er.sqlite_errorname)
            raise er


    def add_child(self,
            first_name: str,
            birth_year: int | None, 
            birth_month: int | None, 
            birth_day: int | None, 
            family_id: int,
            first_id: int | None, 
            second_id: int | None, 
            grade_offset: int = 0,
            ) -> Any:

        '''Python wrapper for queries/add_child.sql. Returns a sql error if one occurs'''

        query = read_queries("add_child")[0]
        try:
            cur = self.con.execute(query,
                             (first_name,
                             birth_year,
                             birth_month,
                             birth_day,
                             family_id,
                             first_id,
                             second_id,
                             grade_offset))
            return cur.fetchall()[0][0]
        except sqlite3.Error as er:

            ic(er.sqlite_errorcode)
            ic(er.sqlite_errorname)
            raise er



