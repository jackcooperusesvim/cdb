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

def new_conn():
    return sqlite3.connect(config.DATABASE_FILEPATH())

def get_query(op: str, table: str) -> str:
    config.CERTIFY_OP_AND_TABLE(op,table)
    filepath = f"queries/{op}/{table}.sql"
    return read_query(filepath)

def init_db():
    connection = new_conn()
    file = read_query("queries/init.sql")
    queries = file.split(";")
    for query in queries:
        exec_query(connection,query)

    connection.commit()

def exec_query(connection : sqlite3.Connection,
               query : str,
               params : list[str] | None = None, return_pd = False) -> sqlite3.Cursor | pd.DataFrame:
    if return_pd:
        return pd.read_sql_query(query,connection, params = params)
    try:
        if params is None:
            cur = connection.execute(query)
        else:
            cur = connection.execute(query,tuple(params))
    except sqlite3.IntegrityError as e:
        raise e
    except Exception as e:
        ic(query)
        if not params is None:
            ic(params)
        raise e


    return cur

def read_query(filepath: str) -> str:
    with open(filepath,'r') as file:
        return file.read()

def read_grade(data):
    b_day = datetime.datetime.strptime(data["birthday"],"%Y-%m-%d").date()+datetime.timedelta(days = 365*data["grade_offset"])

    for name in G.DICT:
        if G.DICT[name][0] < b_day and G.DICT[name][1] > b_day:
            return name
    return "Grad"

def db_action(connection: sqlite3.Connection,
              op: str, 
              table: str, 
              where_id: int | None = None,
              input_options: dict[str,str] | None = None) -> pd.DataFrame | Any:

    MAX_STRIKES = 3
    #TODO: COVER EDGE CASES HERE
    return_pd = False
    if op == "get_data":
        return_pd = True



    query = get_query(op,table)
    slots = config.AVAILABLE_ARGS(op,table)
    params = []

    if where_id != None:
        return_pd = False
        query = query[:len(query)-2]
        query += f" WHERE {table}.id = {int(where_id)};"
        ic(query)

    if input_options != None:
        strikes = 0
        for slot in slots:
            if slot in input_options:
                params.append(input_options[slot])
            else:
                strikes += 1
                if strikes >= MAX_STRIKES:
                    raise Exception(f'you filled {strikes} wrong entries. You\'re out')
                params.append("null")
        out = exec_query(connection,query, params, return_pd = return_pd)
    else:
        out = exec_query(connection,query,return_pd = return_pd)

    if type(out) == sqlite3.Cursor:
        out = out.fetchall()
    if op in ["edit","add"]:
        rep_commit(connection)
    if op == "add":
        out = out[0][0]

    return out


def rep_commit(connection: sqlite3.Connection):
    try:
        connection.commit()
    except sqlite3.OperationalError as e:
        ic(e)






























































































class CoopDb:
    def __init__(self, filepath = None):
        if filepath == None:
            self.filepath = config.DATABASE_FILEPATH()
        else:
            self.filepath = filepath

        self.con = sqlite3.connect(self.filepath)


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
