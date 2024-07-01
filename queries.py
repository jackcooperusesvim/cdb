import sqlite3
import re
from typing import Any
from icecream import ic
import config
import pandas as pd


def exec_query_pandas(connection: sqlite3.Connection,query:str) -> list[pd.DataFrame]:
    results = []
    with open(config.QUERY_DIR()+"/"+query+".sql") as file:
        for query in file.read().split(";"):
            results.append(pd.read_sql(query,connection))
    return results

def rc(Str:str,char:str) -> str:
    return "".join(Str.split(char))

def read_queries(query: str) -> list[str]:
    '''Reads all queries from the .sql file at "config.QUERY_DIR()/{query}.sql"'''
    queries = []
    with open(config.QUERY_DIR()+"/"+query+".sql") as file:
        for query in file.read().split(";"):
            query = rc(rc(query,'\t'),'\n')
            if query != '':
                queries.append(query)
    return queries

class CoopDb:

    def __init__(self, filepath = config.DATABASE_FILEPATH()):
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

    def read_table(self, table: str) -> pd.DataFrame:
        return pd.read_sql(self.con, "SELECT * FROM "+table+" ;")

    def add_class(self,
                  name: str,
                  desc: str | None,
                  hour: int,
                  member_cost: int,
                  regular_cost: int):

        query = read_queries("add_class")[0]

        try:
            ic(query)
            cur = self.con.execute(query,(name,desc,hour,member_cost,regular_cost)) 
            return cur
        except sqlite3.Error as er:
            ic(er.sqlite_errorcode)
            ic(er.sqlite_errorname)



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
                   note: str | None):

        query = read_queries("add_family")[0]

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
            return cur
        except sqlite3.Error as er:
            ic(er.sqlite_errorcode)
            ic(er.sqlite_errorname)


    def add_child(self,
            first_name: str,
            birth_year: int | None, 
            birth_month: int | None, 
            birth_day: int | None, 
            first_id: int | None, 
            second_id: int | None, 
            grades_behind: int = 0) -> Any:

        '''Python wrapper for queries/children.sql. Returns a sql error if one occurs'''

        query = read_queries("add_child")[0]
        try:
            cur = self.con.execute(query,
                             (first_name,
                             birth_year,
                             birth_month,
                             birth_day,
                             grades_behind,
                             first_id,
                             second_id))
            return cur
        except sqlite3.Error as er:

            ic(er.sqlite_errorcode)
            ic(er.sqlite_errorname)



