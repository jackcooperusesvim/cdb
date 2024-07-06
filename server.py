from flask import Flask
from queries import *
from test_queries import generate_testing_db

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

# EDIT MAIN PAGES
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
        html = file.read()
    return html

# TABLE LOADING

@app.route("/get_child_table")
def get_child_table():
    cdb = generate_testing_db()
    return cdb.generate_table_html("children")

@app.route("/get_family_table")
def get_family_table():
    cdb = generate_testing_db()
    return cdb.generate_table_html("families")

