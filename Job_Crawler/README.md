# Jobs Database Web Scrapper & Twitter Bot
AI Skunks Jobs Database

## Web Scrapper

Script 1

The web scrapper takes a list of job keywords from a SQL database (e.g. finance, or machine learning) and a list of cities (e.g. Boston) and scraps job postings from Indeed.com and puts those links into a SQL database.

Script 2

Looks for job urls that have not been visted and scraps job information from a specific job listing and puts that into a SQL database

## Twitter Bot

Bot Script 1
The twitter bot  takes a list of job keywords from a SQL database (e.g. finance, or machine learning) and gets the json for those keywords and saves the json files.


Bot Script 2

Takes the twitter json files and removes duplicates and extracts usefull information and add longitude and latitude and stores the twiiter data in a SQL database

Bot Script 3

Outputs as csv file subsets of the twiiter data (e.g. machine learning tweets from June 1, 20022 to July 1, 2022)
