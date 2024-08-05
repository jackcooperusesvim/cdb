from flask import Flask, request
from queries import *
import html_generators as htmlg

app = Flask(__name__)

@app.route("/")
def index():
    with open("web/index.html","r") as file:
        html = file.read()
    return html
@app.route("/blank")
def nada():
    return ''

@app.route("/htmx")
def htmx():
    with open("web/htmx.min.js","r") as file:
        html = file.read()
    return html

# SEND THE TABLES
@app.route("/table")
def table():
    connection = new_conn()
    try:
        table = request.headers["table"]
    except Exception as e:
        return index()

    out = db_action(connection,"get_data", table)
    if type(out) == pd.DataFrame:
        return htmlg.form_space()+htmlg.html_table(out,table)
    raise Exception("db_action returned sqlite3.Cursor instead of pd.DataFrame")

# SEND THE FORM LOADERS
@app.route("/form_loader")
def form_loader():
    connection = new_conn()
    try:
        ic(request.headers)
        id = int(request.headers["id"])
        ic(request.headers["id"])
        table = request.headers["table"]
        ic(request.headers["table"])
    except Exception as e:
        ic(e)
        return '<h1>ERROR</h1>'

    out = list(db_action(connection,"get_data",table, where_id=id)[0])
    ic(out)
    out_dict = dict()
    out_dict['id'] = out[0]
    for i in range(1,len(out)):
        out_dict[config.AVAILABLE_ARGS("edit",table)[i-1]] = out[i]

    if type(out) == pd.DataFrame:
        raise Exception("db_action returned sqlite3.Cursor instead of pd.DataFrame")

    return htmlg.blank_row(out_dict,table)

# SEND THE FORMS 
@app.route("/form")
def form():
    return '<h1>kachow</h1>'

# RECIEVE THE FORMS 
@app.route("/submit", methods = ['POST'])
def submit():
    return ''













def edit_post():

    ic(request.headers["id"])
    ic(request.headers)

    return htmlg.child_edit_form(int(request.headers["id"]))

# TABLE LOADING
@app.route("/get_child_table")
def get_child_table():
    cdb = CoopDb("test.db")
    ic(cdb.read_table("children"))
    return htmlg.html_table(cdb.disp_children())

@app.route("/submit_child", methods = ["POST"])
def submit_child():
    ic(request.form)
    ic(request.headers["id"])

    return ''


@app.route("/get_family_table")
def get_family_table():
    cdb = CoopDb("test.db")
    return htmlg.html_table(cdb.read_table("families"))

