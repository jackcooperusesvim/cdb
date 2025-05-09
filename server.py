from flask import Flask, request
from queries import *
import html_generators as htmlg
import form_val
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

@app.route("/families_table")
def families_table():
    connection = new_conn()
    out = db_action(connection,"get_data", 'families')
    ic(out)
    ic(out)
    if type(out) == pd.DataFrame:
        return htmlg.html_table(out,'families')
    raise Exception("db_action returned sqlite3.Cursor instead of pd.DataFrame")

@app.route("/children_table")
def child_table():
    connection = new_conn()
    out = db_action(connection,"get_data", 'children')
    ic(out)
    ic(out)
    if type(out) == pd.DataFrame:
        return htmlg.html_table(out,'children')
    raise Exception("db_action returned sqlite3.Cursor instead of pd.DataFrame")

@app.route("/first_hour_table")
def first_hour_table():
    connection = new_conn()
    out = db_action(connection,"get_data", 'first_hour')
    ic(out)
    ic(out)
    if type(out) == pd.DataFrame:
        return htmlg.html_table(out,'first_hour')
    raise Exception("db_action returned sqlite3.Cursor instead of pd.DataFrame")

@app.route("/second_hour_table")
def second_hour_table():
    connection = new_conn()
    out = db_action(connection,"get_data", 'second_hour')
    ic(out)
    ic(out)
    if type(out) == pd.DataFrame:
        return htmlg.html_table(out,'second_hour')
    raise Exception("db_action returned sqlite3.Cursor instead of pd.DataFrame")

@app.route("/new_record_button")
def new_rec_button():
    try:
        table = request.headers["table"]
    except Exception as e:
        ic(e)
        return '<h1>ERROR</h1>'
    return htmlg.add_button(table)


@app.route("/new_record_form")
def new_record_form():
    try:
        table = request.headers["table"]
    except Exception as e:
        ic(e)
        return '<h1>ERROR</h1>'
    ic(table)

    id = -1
    out = "err"
    if table == "children":
        out = htmlg.child_edit_form(id)
    elif table == "families":
        out = htmlg.family_edit_form(id)
    elif table in ['first_hour','second_hour']:
        out = htmlg.class_edit_form(id,table)
    return out


# SEND THE FORM LOADERS
@app.route("/form_loader")
def form_loader():
    connection = new_conn()
    try:
        id = int(request.headers["id"])
        table = request.headers["table"]
    except Exception as e:
        ic(e)
        return '<h1>ERROR</h1>'

    match id:
        case -1:
            return htmlg.add_form_loader(table)
        case _:
            out = list(db_action(connection,"get_data",table, where_id=id)[0])
            ic(out)
            out_dict = dict()
            out_dict['id'] = out[0]
            for i in range(1,len(out)):
                out_dict[config.AVAILABLE_ARGS("get_data",table)[i-1]] = out[i]

            if type(out) == pd.DataFrame:
                raise Exception("db_action returned sqlite3.Cursor instead of pd.DataFrame")
            ic(out_dict)

            return htmlg.blank_row(out_dict,table)

# SEND THE FORMS 
@app.route("/form")
def form():
    try:
        id = int(request.headers["id"])
        table = request.headers["table"]
    except Exception as e:
        ic(e)
        return '<h1>ERROR</h1>'

    out = "ERR"
    ic(table)
    if table == "children":
        out = htmlg.child_edit_form(id)
    elif table == "families":
        out = htmlg.family_edit_form(id)
    elif table in ['first_hour','second_hour']:
        out = htmlg.class_edit_form(id,table)
    return out

# RECIEVE THE FORMS 
@app.route("/submit_new", methods = ['POST'])
def submit_new():
    return ''
@app.route("/submit", methods = ['POST'])
def submit():
    connection = new_conn()
    try:
        form_data = request.form
        table = request.headers['table']
        id = int(request.headers['id'])
        ic(form_data)

    except Exception as e:
        ic(e)
        return '<h1>FRONT_END_ERROR: RESTART PAGE</h1>'
    form_data = dict(form_data)
    ic(form_data)
    err = ''

    try:
        new_data = form_val.validate_form(table,form_data)
        assert id != -1
    except AssertionError:
        #TODO: ADD FUNCTIONALITY FOR ADDING NEW RECORDS
        pass
    except Exception as e:
        err = e
    else:
        ic(new_data)
        db_action(connection,"edit",table,where_id= id, input_options=new_data)
        ic(db_action(connection,"get_data",table,where_id=id))
        connection.commit()
        return htmlg.table_reloader(table)

    if table == "children":
        return htmlg.child_edit_form(id, err = str(err))
    elif table == "families":
        return htmlg.family_edit_form(id, err = str(err))
    elif table in ['first_hour','second_hour']:
        return htmlg.class_edit_form(id, table, err = str(err))

@app.route("/blank_endpoint")
def be():
    return ''

