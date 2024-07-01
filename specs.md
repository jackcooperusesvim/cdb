# Specifications


## Automatic Classification

Automatically calculate who goes in which class according to birthday (with a system for exemptions for Developmental Disorders)

## Macros

### Enter Families
    - enter last name

Enter families through forms
    Require manual "pushing" for

Parent data

Family Data
    id
    Parent_Mn
    Parent_Sec
    Last Name
    Street
    City
    State
    ZIP
    Phone1
    Phone2
    Phone3 (opt)
    Email
    is_Member

Child-Family Table
Parent-Family Table

Child Table
    id
    First Name DOB
    Offset
    1st Hr FK
    2nd Hr FK

Class Data 
    id
    Name
    Hour
    Member Cost
    Regular Cost

distinguish families that are in from those who aren't
