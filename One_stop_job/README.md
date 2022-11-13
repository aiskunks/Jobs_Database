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


The osj account has a login and password. This login is the same as a user’s Twitter handle. The Twitter handle is unique – hence it can also be treated as the primary key of the table.

A user can apply to a job through Twitter by applying through ‘job_url’. This job URL mentioned in a tweet is stored in ‘tweet_url’ table. Every tweet that has a URL in it, will have an entry in ‘tweet_url’ table.

‘jobs_applied’ has the ‘application_tweet_id’ of the tweet which uniquely distinguishes each tweet, ‘job_url’ which is a foreign key reference to the ‘job_url’ in ‘tweet_url’ table.

A user can tweet (save) how many ever jobs he/she wants and add them to ‘my_saved_applications’. Hence ‘my_saved_applications’ has a composite key with is a combination of both ‘job_tweet_id’ and ‘user_handle’ in the table.


UML diagram:

<img width="508" alt="image" src="https://user-images.githubusercontent.com/113729244/201505797-7f5bc66f-76a6-451c-9a33-08d6c83e09b6.png">

SQL Statements for the conceptual model:

•tweets_table:

 CREATE TABLE `tweets_table` (
  `tweet_id` bigint NOT NULL,
  `recruiter_twitter_handle` varchar(64) DEFAULT NULL,
  `tweet_text` varchar(1000) DEFAULT NULL,
  `tweet_date` timestamp NULL DEFAULT NULL,
  `profile_image_url` varchar(256) DEFAULT NULL,
  `recruiter_tweet_location` varchar(50) DEFAULT NULL,
 PRIMARY KEY (`tweet_id`) );
 
•tweets_tags:

 CREATE TABLE `tweet_tags` (
  `tweet_id` bigint NOT NULL,
  `tags` varchar(256) DEFAULT NULL,
   PRIMARY KEY (`tweet_id`),
   CONSTRAINT `USER_TAG_CONSTRAINT` FOREIGN KEY (`tweet_id`) REFERENCES `tweets_table` (`tweet_id`) );

•job_urls:

 CREATE TABLE `job_urls` (
  `tweet_id` bigint DEFAULT NULL,
  `job_url` varchar(256) NOT NULL,
   PRIMARY KEY (`job_url`),
   KEY `TWEET_URL_CONSTRAINT` (`tweet_id`),
  CONSTRAINT `TWEET_URL_CONSTRAINT` FOREIGN KEY (`tweet_id`) REFERENCES `tweets_table` (`tweet_id`) );

•osj_acount:

CREATE TABLE `osj_account` (
  `twitter_handle` varchar(256) NOT NULL,
  `password` varchar(256) DEFAULT NULL,
  `role` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`twitter_handle`) );

•osj_users:

CREATE TABLE `osj_users` (
  `twitter_handle` varchar(256) NOT NULL,
  `screen_name` varchar(256) DEFAULT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `location` varchar(128) DEFAULT NULL,
  `joined_date` timestamp NULL DEFAULT NULL,
  `user_id` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`twitter_handle`),
  CONSTRAINT `USER_CONSTRAINT` FOREIGN KEY (`twitter_handle`) REFERENCES `osj_account` (`twitter_handle`) );

•my_saved_applications:

CREATE TABLE `my_saved_applications` (
  `job_tweet_id` bigint NOT NULL,
  `recruiter_twitter_handle` varchar(256) DEFAULT NULL,
  `user_handle` varchar(256) NOT NULL,
  `post_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`job_tweet_id`,`user_handle`),
  KEY `SAVED_URL_CONSTRAINT` (`user_handle`),
  CONSTRAINT `JOB_TWEET_ID_CONSTRAINT` FOREIGN KEY (`job_tweet_id`) REFERENCES `tweets_table` (`tweet_id`) );

•jobs_applied:

CREATE TABLE `jobs_applied` (
  `application_tweet_id` bigint NOT NULL,
  `job_url` varchar(256) DEFAULT NULL,
  `user_twitter_handle` varchar(256) DEFAULT NULL,
  `applied_tweet_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`application_tweet_id`),
  KEY `JOBS_APPLIED_CONSTRAINT` (`job_url`),
  CONSTRAINT `JOBS_APPLIED_CONSTRAINT` FOREIGN KEY (`job_url`) REFERENCES `job_urls` (`job_url`) );

USE CASE, SQL QUERIES and RELATIONAL ALGEBRA:

1. NAMITHA J C

