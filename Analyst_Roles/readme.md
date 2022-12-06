# Title: Analyst Directory (The Jobs Database)

## Team Members: 

| Team member         | Email                         | NUID | 
| ------------------  | ----------------------------- | ---------- |
| Srushty Returi      | returi.s@northeastern.edu     | 002749457  |
| Swatika Ayyappan    | ayyappan.s@northeastern.edu   | 002783598  |
| Rishabh Pandey      | pandey.risha@northeastern.edu | 002743847  |
| Kshitijkumar Tiwari | tiwari.ks@northeastern.edu    | 002743158  |


**Tools**: MySQL, Jupyter Notebook and Matplot 

## Project Scope:

The goal of this project is to create a database to help "Prospective Job Seekers" to find their dream role with an ease using the database that is designed for analyst jobs in our project.

## Project Description:

•	The jobs database will include all the details of various analyst job positions like salary, job description, degree requirements, number of openings, locations etc.

•	The data for the database will be web scraped from multiple job portals like LinkedIn, Monster, Indeed and other job portals using python.

•	 Also, the data can be used to predict suitable job roles for the users based on their skill sets using Machine Learning.


# Assignment 3 - Gathering, Scraping, Munging and Cleaning Data

## Jobs Database for Analyst Jobs:

This database will contain all the jobs having the keyword ‘analyst’ in the title.

All the attributes of the job information like location, salary, job-type, etc. are included in the tables.

The database includes data scraped from various websites and data from various downloadable sources like data repositories.

The project files include Create_Insert_Queries.docx that consists of all the create and insert queries for the database, Jobs_Database_UML_Diagram.pdf which is the model for the database, Use_Cases.docx which contains the new usecases and 5 jupyter notebooks.

The project consists of 5 main jupyter notebooks which are:


## First notebook (Glassdoor_Webscrapping_BS.ipnyb):

The data from ‘glassdoor.com’ is scraped using BeautifulSoup.
The data collected from scraping is cleaned using python script and stored in lists.
Cleaned data is audited and checked for accuracy before going further. 
The data stored in lists are stored in a DataFrame using the ‘pandas’ library.
Using the ‘sqlalchemy’ library these dataframes are added to the connected database.
Also, DataVisualisation for various columns like ‘job_position’ and ‘company_name’ and their count is done using the ‘plotly’ library.

## Second notebook (Glassdoor_Rating_Review.ipnyb):

The ratings and reviews are collected from a data repository. 
Collected data is visually represented using the ‘matplotlib’ library.

## Third notebook (Job_data_Data_Repository.ipnyb):
The data downloaded from data repositories is read into the notebook using pandas.
The data collected is cleaned using python script and stored in lists.
Cleaned data is audited and checked for accuracy before going further.
The data stored in lists are stored in a DataFrame using the ‘pandas’ library.
Using the ‘sqlalchemy’ library these dataframes are added to the connected database.


## Fourth Notebook (Jobs_Database_Data_Repository_1.ipnyb):
The data downloaded from data repositories is read into the notebook using pandas.
The data collected is cleaned using python script and stored in lists.
Cleaned data is audited and checked for accuracy before going further.
The data stored in lists are stored in a DataFrame using the ‘pandas’ library.
Using the ‘sqlalchemy’ library these dataframes are added to the connected database.


# Fifth notebook (Sample_data.ipnyb):
This notebook contains sample screenshots for all the data used for making the database.

The Assignment folder also contains data downloaded from data repositories which are used in the codes.


