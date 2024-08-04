import sqlite3
import re
from typing import Any, Callable
from icecream import ic
import config
import pandas as pd
import datetime
from enum import Enum
import time

import datetime

from gradedates import G
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

def read_grade(data):

    b_day = datetime.datetime.strptime(data["birthday"],"%Y-%m-%d").date()+datetime.timedelta(days = 365*data["grade_offset"])

    for name in G.DICT:
        if G.DICT[name][0] < b_day and G.DICT[name][1] > b_day:
            return name
    return "Grad"

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

    def disp_children(self):
        data = self.read_table("children")
        data["grade"] = data.apply(read_grade, axis = 1)
        del data["grade_offset"]
        return data

    def disp_child(self, id: int):
        data = self.disp_children()
        data = data[data["id"]==id]
        return data

    def find_children(self, fam_id: int):
        query = read_queries("find_children")[0]

        try:
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
            birthday: datetime.date, 
            family_id: int,
            first_id: int | None, 
            second_id: int | None, 
            grade_offset: int = 0,
            ) -> Any:

        '''This function will add/change the '''

        query = read_queries("add_child")[0]
        try:
            cur = self.con.execute(query,
                             (first_name,
                             str(birthday),
                             family_id,
                             first_id,
                             second_id,
                             grade_offset))
            return cur.fetchall()[0][0]
        except sqlite3.Error as er:

            ic(er.sqlite_errorcode)
            ic(er.sqlite_errorname)
            raise er

    def edit_child(self,
            first_name: str | None,
            birthday: datetime.date| None, 
            family_id: int | None,
            first_id: int | None, 
            second_id: int | None, 
            grade_offset: int | None,
                   id: int):
        cur = self.con.execute("SELECT count(first_name) FROM children")
        print(cur.fetchall)
