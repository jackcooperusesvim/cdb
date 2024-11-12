import sqlite3
from icecream import ic
import config
import pandas as pd
from typing import Any
import libsql_experimental as libsql

def new_conn():
    return sqlite3.connect(config.DATABASE_FILEPATH())
def new_turso_conn():
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
def init_turso_db(url: str, token: str):
    connection = libsql.connect(url,auth_token=token)
    file = read_query("queries/init.sql")
    queries = file.split(";")
    for query in queries:
        exec_query(connection,query)


def exec_query(connection : sqlite3.Connection | libsql.Connection,
               query : str,
               params : list[str] | None = None, return_pd = False) -> sqlite3.Cursor | libsql.Cursor | pd.DataFrame:

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
        if not params is None:
            ic(params)
        raise e


    return cur

def read_query(filepath: str) -> str:
    with open(filepath,'r') as file:
        return file.read()

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
                errstr = f"{slot} was expected and is not present db_action input"
                ic(errstr)
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
        rep_commit(connection)







