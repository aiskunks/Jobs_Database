One Stop Job (addition to Job database)

Team members: Namitha J C (NUID – 002795461)
		 Sinchana Kumara (NUID – 002780971)
		 Maheswara Sai Ram Palakurthy (NUID – 002772768)

Github Id’s: Njc27
	       SinchanaKumara
	       maheswarpalakurthy

ReadMe Document: 

The objective of this project is to create a database for job finders where they need to type in the job role and select from which job sites they will apply for that job. The database will consist data from the most visited job sites like Indeed, Glassdoor, Monster etc., with columns Job Id, Job role, Job Description, Skills, Company, Location, Job site (link to the site). 

Using BeautifulSoup in python, we scrape the necessary data required and store them in a csv file. Later this csv file is cleaned from duplicate and null values. By then storing this data in a sql table we can perform the necessary operations such as : Searching and Filtering the data.



##Assignment - 2

A model of job database – one stop job using Twitter:

ER diagram:

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/201505723-2c050c31-259b-4f52-a819-f70a4f2def0f.png">


•	The osj account has a login and password. This login is the same as a user’s Twitter handle. The Twitter handle is unique – hence it can also be treated as the primary key of the table.
•	A user can apply to a job through Twitter by applying through ‘job_url’. This job URL mentioned in a tweet is stored in ‘tweet_url’ table. Every tweet that has a URL in it, will have an entry in ‘tweet_url’ table.
•	‘jobs_applied’ has the ‘application_tweet_id’ of the tweet which uniquely distinguishes each tweet, ‘job_url’ which is a foreign key reference to the ‘job_url’ in ‘tweet_url’ table.
•	A user can tweet (save) how many ever jobs he/she wants and add them to ‘my_saved_applications’. Hence ‘my_saved_applications’ has a composite key with is a combination of both ‘job_tweet_id’ and ‘user_handle’ in the table.


UML diagram:

<img width="508" alt="image" src="https://user-images.githubusercontent.com/113729244/201505797-7f5bc66f-76a6-451c-9a33-08d6c83e09b6.png">

SQL Statements for the conceptual model:

