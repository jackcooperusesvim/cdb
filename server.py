from flask import Flask, request
from queries import *
import html_generators as htmlg
import gradedates

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
        ic(request.headers)
        raise e

    out = db_action(connection,"get_data", table)
    ic(out)
    if type(out) == pd.DataFrame:
        return htmlg.html_table(out,table)
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
        out_dict[config.AVAILABLE_ARGS("get_data",table)[i-1]] = out[i]

    if type(out) == pd.DataFrame:
        raise Exception("db_action returned sqlite3.Cursor instead of pd.DataFrame")

    return htmlg.blank_row(out_dict,table)

# SEND THE FORMS 
@app.route("/form")
def form():
    try:
        ic(request.headers)
        id = int(request.headers["id"])
        ic(request.headers["id"])
        table = request.headers["table"]
        ic(request.headers["table"])
    except Exception as e:
        ic(e)
        return '<h1>ERROR</h1>'

    out = ""
    if table == "children":
        out = htmlg.child_edit_form(id)
    elif table == "families":
        out = htmlg.family_edit_form(id)
    elif table in ['first_hour','second_hour']:
        out = htmlg.class_edit_form(id,table)
    return out

# RECIEVE THE FORMS 
@app.route("/submit", methods = ['POST'])
def submit():
    connection = new_conn()
    try:
        form_data = request.form
        table = request.headers['table']
        ic(form_data)

    except Exception as e:
        ic(e)
        return '<h1>ERROR</h1>'

    form_data = dict(form_data)
    ic(form_data)
    out_data = dict()
    error = None

    for i in form_data:
        out_data[i] = form_data[i]
    try:
        out_data["id"] = int(form_data["id"])
    except:
        error = "bad id"

    if table == 'families':
        try:
            out_data["phone1"] = int(form_data["phone1"])
            assert out_data["phone1"] < 9999999999 and out_data["phone1"] > 1000000000
        except:
            error = "Primary Phone is invalid (must be a no punctuation with 10 digits)"

        try:
            out_data["phone2"] = int(form_data["phone2"])
            assert out_data["phone2"] < 9999999999 and out_data["phone2"] > 1000000000
        except:
            error = "Second Phone is invalid (must be a no punctuation with 10 digits)"

        try:
            out_data["phone3"] = int(form_data["phone3"])
            assert out_data["phone3"] < 9999999999 and out_data["phone3"] > 1000000000
        except:
            try:
                del out_data["phone3"]
            except:
                error = "Tertiary Phone is invalid (must be a no punctuation with 10 digits)"

    elif table == 'children':

        try:
            out_data["first_id"] = int(form_data["first_id"])
            #TODO: CHECK IF THE ID IS LEGIT
        except:
            error = "first_id is not valid"

        try:
            out_data["second_id"] = int(form_data["second_id"])
            #TODO: CHECK IF THE ID IS LEGIT
        except Exception as e:
            error = f"second_id ({out_data["second_id"]}) is not valid"
            raise e

        try:
            out_data["family_id"] = int(form_data["family_id"])
            #TODO: CHECK IF THE ID IS LEGIT
        except Exception as e:
            error = f"family_id ({form_data["family_id"]}) is not valid"
            raise(e)

        try:
            bday = gradedates.str_to_dt(form_data["birthday"])
            offset = gradedates.from_grade(bday,form_data["grade"])
            out_data["birthday"] = str(bday)
            out_data["grade_offset"] = offset
            #TODO: CHECK IF THE ID IS LEGIT
        except Exception as e:
            error = f"birthday ({form_data["birthday"]})is not valid"
            raise e

    elif table in ['first_hour','second_hour']:

        try:
            out_data["member_cost"] = int(form_data["member_cost"]*100)/100
        except:
            error = "member_cost must be a valid amount of money (must be a decimal in increments of 0.01"

        try:
            out_data["regular_cost"] = int(form_data["regular_cost"]*100)/100
        except:
            error = "regular_cost must be a valid amount of money (must be a decimal in increments of 0.01"
    ic(error)

    id = out_data["id"]
    del out_data["id"]

    if error is None:
        #TODO: ADD TO DATABASE
        ic(out_data)
        db_action(connection,'edit',table,input_options= out_data, where_id = id)
        connection.commit()
        return f'<div {htmlg.headers(id=None,table = table)} hx-trigger="load" hx-swap="outerHTML" hx-get="/table" hx-target=".table"></div>'

    else:

        ic(error)
        out = f"<h3>ERROR: {error}</h3>"
        if table == "children":
            out += htmlg.child_edit_form(id)
        elif table == "families":
            out += htmlg.family_edit_form(id)
        elif table in ['first_hour','second_hour']:
            out += htmlg.class_edit_form(id,table)
        return out

@app.route("/blank_endpoint")
def be():
    return ''

