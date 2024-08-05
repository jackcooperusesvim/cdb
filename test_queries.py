import queries
from icecream import ic

tdb = queries.CoopDb("test.db")

get_child_form_data = queries.exec_query_pandas(tdb.con, "get_child_form_data")

ic(get_child_form_data)
 = queries.exec_query_pandas(tdb.con, "get_child_form_data")
