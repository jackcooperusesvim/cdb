# Co-op Db - IN THE WORKS

This is not an open source project. It is a personal project which I am sharing over github. No PRs, no contributions.


cdb is a database system which I am writing for a local homeschool co-op. It is a Python-driven localhost web-app (I think thats the proper title), which uses a SQLite3 database, Python backend (with Flask), and a UI built with HTMX. The end goal of this system is to replace the dysfunctional excel sheet which the co-op currently uses with a simple, practical, and reliable UI; cutting down the data work down from several hours a week to a couple minutes a month.


## Notes:

There are 3 overall parts to building this system
    The Database Interactor (simplifies database interactions; found in queries.py)
    The backend (utilizes DBI methods and the Flask framework to serve data to the frontend)
    The UI

Some may be wondering why I decided to do this mental split on the backend. The reason for this is that there is quite a bit of computation and general datetime confusion (I hate datetime data) 
    that I would prefer to handle as seperately as possible and doing this split where all database interactions are highly simplified through a sort of library 
    helps me focus on one task at a time during development (a seperation of concerns, if you will) and will hopefully mean a more resilient end product

Immediate To-do:
- [ ]  Write test for datetime and grade calculations
    - [ ] make datetime and grade calculations bidirectional
- [ ] add a method to CoopDb for adding classes
- [ ] add a method to CoopDb for editing data

General To-do:
- [ ] build a UI (I imagine I will be using htmx)
- [ ] design a server to serve the data (Using flask)
    - [ ] Find a library to use for pretty prints of tabular data to serve to the UI

## File Summary

* queries/ - all the SQL queries are written in files for easier debugging and syntax highlighting 
* config.py - All constants and things which may need to be changed in the future are stored in functions here
    (e.g. what day co-op starts, the database filepath, the names of each individual grade)
* gradedates.py - Handles all constants regarding datetime and grade calculations*
    *When I say constants, I refer to constants for the time period of use, these values change over time, but not over the course of time between opening and closing the application
* queries.py - the CoopDb class from this file handles all SQL queries and provides an abstraction for the database queries
* test_queries.py - integration tests for the CoopDb class from queries.py






