from flask import Flask, request
from queries import *
import html_generators as htmlg

app = Flask(__name__)

@app.route("/")
def index():
    with open("web/index.html","r") as file:
        html = file.read()
    return html

@app.route("/htmx")
def htmx():
    with open("web/htmx.min.js","r") as file:
        html = file.read()
    return html

# MAIN PAGES DB EDITOR
@app.route("/child_edit")
def child_edit():
    with open("web/child_edit.html","r") as file:
        html = file.read()
    return html

@app.route("/family_edit")
def family_edit():
    with open("web/family_edit.html","r") as file:
        html = file.read()
    return html

@app.route("/class_edit")
def class_edit():
    with open("web/class_edit.html","r") as file:
        return file.read()

# EDIT MAIN PAGES
@app.route("/edit_child")
def edit():
    db = CoopDb("test.db")
    id = int(request.headers["id"])

    out = htmlg.blank_row(db.disp_child(id))
    return out

@app.route("/form_edit_child")
def form_edit():
    id = int(request.headers["id"])
    return htmlg.child_edit_form(id)

@app.route("/editpost", methods = ['POST'])
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

@app.route("/get_family_table")
def get_family_table():
    cdb = CoopDb("test.db")
    return htmlg.html_table(cdb.read_table("families"))

