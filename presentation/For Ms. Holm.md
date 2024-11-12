# The Co-op Database:
The Excel spreadsheet which the Co-Op uses for their student and family data is a mess. Ms. Moreau was really the only person who understood it, and since she left, the spreadsheet has been taking exorbitant amounts of time from the rest of the group. Something needs to be done. The following is an analysis of the current state of the database, an exploration of potential solutions, and my proposition for a minimal, scalable, solution.

## The Current State:
So what is this spreadsheet and how does the co-op use it? This spreadsheet stores all the information for every family in the co-op. This includes the names of all the children, and all the classes each individual child is taking. Every year, data is downloaded from Google Forms and manually typed into the database with a macro. As the year goes on, that same macro is used to edit the existing data and update the various schedules, contact lists, and other useful tables for co-op organizers. In a way, the data cannot be said to be stored in one place: the data found in the contact list is not sourced from the data in the "database" in any way. It is it's own database, storing it's own subset of the data, which receives updates from the same macro which updated all the other databases in the Excel workspace.

## The Issues and Solutions:
The first problem, which I already hinted at, is that the database does not perform the core function of a database. At the core of the ideal of the database is its function as a Single Source of Truth (SSOT). Any piece of data you get from the database should be traceable back to a single data-point in storage. No information should be stored twice. In the Excel sheet, data is loaded into a macro, then various fields are duplicated into various different presentations. This problem of Data Duplication makes the data incredibly fragile and incredibly complex to update and fix.

The second problem with the database is that both the input form and the input macros are inflexible. This is a problem because the number of children in a family is flexible. Every time the standing record for the largest co-op family is broken, the entire database system of macros must be essentially rebuilt from the ground up. This is no bueno.

The good news is that both of these problems are easily solvable at the database level by building a system around a normalized relational database. My recommendation is to use a free cloud platform for this (Turso, Xata, etc.). I recommend Xata, which is free (for the amount of data we will have) and comes with a simple spreadsheet-like UI. Reports can then be generated off of this Database, but we will have to choose a method.

## Decisions, Decisions, Decisions...
### How far are we willing to go?

This is the biggest question to answer, and it isn't so simple as just saying "we want to automate as much as we can and build everything from scratch". There are tradeoffs and very few single developers (especially not a junior like myself) can (or would be willing) write a complex full-stack application on short notice. Do you want to load data into the database automatically without typing in each entry? Simple, we write some scripts, and run them whenever the data needs to be loaded. Now, what if you want to automatically calculate billing and send invoices? Well, that level of complexity requires the development of a web application, which requires _**far**_ more work and area-specific expertise, and is going to incur more cost, and involve more maintenance than a simple cloud database with some scripts. 

Here I have made a list of features and optimizations and the level of complexity they require, along with some information about the different considerations and expectations that come inherent to each level of complexity.

One last thing to note is that when looking at features: the development time is not linear. Implementing 2 features approximately equal in complexity will not take 2x the time as 1 would take. It will take more like 3x, and those inefficiencies of scale will increase even more with more features. 
### Potential Features

**Report Generation**
	Function:
		Generating reports, calendars, and contact lists
	Options:
		1. Generation Scripts
			This would be done on-level with a Lv. 2 Solution
		1. Lv. 4 Website "Reports" page
			The algorithms will require quite a bit of time
			Hosting costs will increase
			
**Automated Data Loading (Getting the data from the beginning of the year into the database)**
	Function:
		Obtaining the data from the User at the beginning of the year and loading it into the database (making ready for authorization from co-op authorities)
	Options:
		1. Manual Entry with Google Forms (Current System)
		2. Automate it with Google Forms
			API costs $10 per month
		3. Automate it with a Website
			Necessitates Lv. 4 of Complexity but aside from those inherent difficulties, it is not difficult. Hosting costs may increase
			
**Class Switching, Swapping, and Locking-In**
	Function:
		Dealing with parents who want their children to change classes. This is currently done manually, and it is feasible to do so
	Options:
		1. Manual Entry with Xata Database Editor
		2. Do it with a Lv. 4 Website
			The algorithms will require quite a bit of time
			Hosting costs will increase

**Payment Systems**
	Function:
		Managing, tracking, and making payments. There are degrees of automation which are possible here.
	Options:
		1. Manage and keep track Payment Separately from the Database
		2. Partial Automation with Xata Data UI
			This is a low-effort / high-reward solution whereby the database *keeps track* of payments by calculating the total cost for the year for any given family, and allows manual entry for keeping track of payments.
		1. Automated with a Lv. 4 Website and Payment API
			API will likely skim a little off the top
			This is a complex task, and will take a couple weeks solo
### Levels of Complexity
1. Manual Entry (No dev time)

2. Local Scripts (2 weeks dev time)
	Development Considerations
	- Providing and maintaining Documentation 
	User Considerations
	- Type of computer being used (may require MacOS or Linux)
	- Documentation and (possibly) training is required
	
3. Inward (Co-op Leadership) facing Web Application 
	Development Considerations (4+ weeks dev time)
	- Few Web Security Concerns
	- Web Hosting (may incur costs)
	- Maintenance of logins
	User Considerations
	- Administrators need a username and password (created by the developer)
	
4. Outward (Co-op Leadership) facing Web Application
		A website with both an administration side and a Parent Dashboard where parents can perform various actions
	Development Considerations (4+ weeks dev time)
	- Requires the development of a CI/CD Pipeline to ensure that bugs are easy to fix. (3 weeks for the unexperienced)
	- Many Web Security Concerns
	- Web Hosting (will incur costs)
	- Documentation and using simple design which requires low training
	- Maintenance of logins
	User Considerations
	- Administrators will need a username and password (created by the developer)

## My Proposition - A Minimal and Scalable Solution:

I have decided that the best way to approach a Proof-of-Concept is with a Level 2 solution consisting of a Google Forms Data Loader, Cloud Database (accessible via UI), a repository of scripts and relevant documentation. This gives us all the functionality of the old Excel Sheet with one easy-to-implement and high-impact feature. This is also a very extensible setup, from which we can add more features as desired after the proof-of-concept. I understand that there are a lot of things and features which are expected of this project, and that this solution may be underwhelming. Below, you will see the options I have elected to use. I expect this initial system to be up and running in ~2 weeks or on Sept 20, at which time I can train whoever needs it.

**Report Generation**
Function: Generating reports, calendars, and contact lists  
Solution: Generation Scripts

**Automated Data Loading**
Function: Getting and loading the data from the user at the beginning of the year  
Solution: Automation with Google Forms API Scripts ($10 per month)  

**Class Switching, Swapping, and Locking-In**
Function: Dealing with parents who want their children to change classes.  
Solution: Manual Entry with Xata UI
  
**Payment Systems**
Function: Managing, tracking, and making payments.  
Solution: Automation of yearly cost calculation

_Note: This is a low-effort / high-reward solution whereby the database **keeps track** of dues by calculating the total cost for the year for any given family, and allows manual entry of payment amounts into the database by an administrator._

### Level of Complexity

2. Local Scripts (2 weeks dev time)  
    Development Considerations
    - Providing and maintaining Documentation  
        User Considerations
    - Type of computer being used (may require MacOS or Linux)
    - Documentation and (possibly) training is required
![[Report Generation]]
