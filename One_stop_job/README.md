# One Stop Job (addition to Job database)

Team members: Namitha J C (NUID – 002795461)
		 Sinchana Kumara (NUID – 002780971)
		 Maheswara Sai Ram Palakurthy (NUID – 002772768)

Github Id’s: Njc27
	       SinchanaKumara
	       maheswarpalakurthy

ReadMe Document: 

The objective of this project is to create a database for job finders where they need to type in the job role and select from which job sites they will apply for that job. The database will consist data from the most visited job sites like Indeed, Glassdoor, Monster etc., with columns Job Id, Job role, Job Description, Skills, Company, Location, Job site (link to the site). 

Using BeautifulSoup in python, we scrape the necessary data required and store them in a csv file. Later this csv file is cleaned from duplicate and null values. By then storing this data in a sql table we can perform the necessary operations such as : Searching and Filtering the data.



# Assignment - 2

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

##Maheswara Sairam Palakruthy

1. Select t.recruiter_twitter_handle, t.tweet_text, t.tweet_date, t.profile_image_url, j.job_url from tweets_table AS t, job_urls AS j where recruiter_twitter_handle = 'SAICjobs' AND t.tweet_id = j.tweet_id;

Use Case: View the details of tweeted handle, such as handle-name ,text ,tweeted date, user-profile-image-url and links present in the tweet posted by “SAICjobs”.
Description: User views the list of data related to the tweet posted by  “#SAICjobs”.
Actor: User
Precondition: User “SAICjobs” should be present and should have posted tweets.
Steps:
Actor action: User views the list of tweet data posted by “SAICjobs”.
System Responses: The list of data for all the tweets posted by “SAICjobs” are displayed.
Alternate Path: There are no orders made by a user.
Error: No history of orders available.

π t . recruiter_twitter_handle, t . tweet_text, t . tweet_date, t . profile_image_url, j . job_url
 σ recruiter_twitter_handle = "SAICjobs" AND t . tweet_id = j . tweet_id
  (ρ t tweets_table ×
   ρ j job_urls)
   
<img width="348" alt="image" src="https://user-images.githubusercontent.com/113727586/201506678-e4e68ee9-d791-4d3c-93ae-a50897602393.png">

2. Select A.twitter_handle, B.recruiter_twitter_handle, A.location from osj_users A, tweets_table B where A.twitter_handle <> B.recruiter_twitter_handle and A.location = B.recruiter_tweet_location ORDER BY A.location;

Use Case: Displaying all the tweets with the same location as the User.
Description: User view tweets from his locality.
Actor: User
Precondition: Jobs must be present in the user location.
Steps:
Actor action: View Jobs with location same as the User.
System Responses: The list of Jobs based on the same location as the user are displayed.
Alternate Path: There are no latest jobs postings.
Error: No Jobs available from the given location.

τ a . location
 π a . twitter_handle, b . recruiter_twitter_handle, a . location
  σ a . twitter_handle <> b . recruiter_twitter_handle AND a . location = b . recruiter_tweet_location
   (ρ a osj_users ×
    ρ b tweets_table)
  
<img width="366" alt="image" src="https://user-images.githubusercontent.com/113727586/201506690-480a4237-6a0d-4ff3-9853-444af1fb415d.png">

3. Select job_url From job_urls Where tweet_id IN (Select tweet_id From tweets_table where tweet_id IN (Select tweet_id from tweet_tags where tags = '#databaseJobs'));

Use Case: View the links attached to the tweet with the hashtag “#databaseJobs”
Description: User views the links related to the hashtag “#databaseJobs”
Actor: User
Precondition: Tweets must be present with the above hashtag.
Steps:
Actor action: User views all the links for a particular hashtag.
System Responses: The links for the Tweets with hashtags.
Alternate Path: There are no orders made by a user.
Error: No history of orders available.

π job_url
 σ tweet_id IN  (π tweet_id
 σ tweet_id IN (π tweet_id
 σ tags = "#databaseJobs" tweet_tags) tweets_table) job_urls

<img width="380" alt="image" src="https://user-images.githubusercontent.com/113727586/201506704-e6c8fe3b-6560-482e-ba7e-26df3bf62138.png">

4. Select * from tweets_table where tweet_text LIKE '%database%';

Use Case: Display all the jobs with keywords “database” in them.
Description: User can view and search  all the job postings with keyword “database” in them.
Actor: User
Precondition: Jobs with keyword “database” must be present .
Steps:
Actor action: User can view Jobs based on keyword “database”.
System Responses: Display all the job postings with keyword “database”.
Alternate Path: Job postings are shown as null or none.
Error: Jobs data unavailable at the moment.

σ tweet_text LIKE "%database%" tweets_table

<img width="382" alt="image" src="https://user-images.githubusercontent.com/113727586/201506725-94abc8c9-aba9-4a45-a156-bc7c06afc57c.png">

5. Select * from tweets_table where tweet_date >= NOW() - INTERVAL 2 DAY;

Use Case: Display all the job postings from the last 2 days.
Description: Job postings from the last 2 days are displayed.
Actor: User
Precondition: There must be jobs posted in the last 2 days.
Steps:
Actor action: User can filter Jobs based on the last 48 hours.
System Responses: Display the Jobs for the last 2 days.
Alternate Path: No Jobs posted in the given days.
Error: No Jobs available now.

σ tweet_date = π date σ date - now() tweets_table

<img width="400" alt="image" src="https://user-images.githubusercontent.com/113727586/201506735-d7dd016e-e92b-406b-bf5f-372704ff2845.png">


##NAMITHA J C

1. Select DISTINCT recruiter_twitter_handle from tweets_table order by recruiter_twitter_handle;

Use Case: View the recruiter handles in the database.
Description: User views all the recruiter handles present in the database.
Actor: User
Precondition: Database must of data for the twitter handles.
Steps:
Actor action: User views all the recruiter handles.
System Responses: The list of all recruiter handles are displayed to user.
Alternate Path: There are no orders made by a user.
Error: No history of orders available.

δ
 τ recruiter_twitter_handle
  π recruiter_twitter_handle tweets_table
  
  <img width="398" alt="image" src="https://user-images.githubusercontent.com/113727586/201506244-143db2ea-587e-4c9d-b0a6-ada43314c45b.png">

2. Select * from tweets_table where tweet_id IN (Select tweet_id from tweet_tags where tags = '#paidinternships');

Use Case: View the tweets attached to the tweet with the hashtag “#paidinternships'”
Description: User views the tweets related to the hashtag “#paidinternships'”
Actor: User
Precondition: Tweets must be present with the above hashtag.
Steps:
Actor action: User views all the links for a particular hashtag.
System Responses: The list for the Tweets with hashtags.
Alternate Path: There are no orders made by a user.
Error: No history of orders available.

σ tweet_id IN (π tweet_id
 σ tags = "#paidinternships" tweet_tags)  tweets_table

<img width="410" alt="image" src="https://user-images.githubusercontent.com/113727586/201506271-5345eb9d-7e2f-4ad3-80f3-4353bf8ca829.png">

3.	Select t.recruiter_twitter_handle, Count(application_tweet_id) AS 'NO. Of Applications' from tweets_table as t RIGHT JOIN job_urls as j ON t.tweet_id = j.tweet_id RIGHT JOIN jobs_applied as ja ON ja.application_tweet_id = j.tweet_id Group BY t.recruiter_twitter_handle;

3.Use Case: Displaying the user Applied job count with respect to recruiter.
Description: User can Applied job count with respect to recruiter.
Actor: User
Precondition: User must have completed Job applications.
Steps:
Actor action: View Applied Job count and its recruiter.
System Responses: The Count of Applications completed with respect to recruiter is displayed.
Alternate Path: User has not applied to any jobs.
Error: Completed applications are not available as of now.

π t . recruiter_twitter_handle, COUNT (application_tweet_id)
 γ COUNT (application_tweet_id) tweets_table  as no_of_Applications
(ρ t tweets_table ⋈ t . tweet_id = j . tweet_id
   ρ j job_urls)

<img width="404" alt="image" src="https://user-images.githubusercontent.com/113727586/201506281-e890ed96-8962-4f72-a7c6-3deb8312b3c4.png">

4.	Select * from osj_users where joined_date between '2022-11-09' and '2022-11-13';

Use Case: Display users who have joined between November 9th 2022 and November 13th 2022.
Description: Filter users based on joined date.
Actor: Admin
Precondition: User must have the field Joined Date.
Steps:
Actor action: Admin can filter users based on joined date.
System Responses: Display all the users joined between the specified date.
Alternate Path: No Users are Displayed.
Error: User Data unavailable.

σ "2022-11-09" <= joined_date AND joined_date <= "2022-11-13" osj_users

<img width="395" alt="image" src="https://user-images.githubusercontent.com/113727586/201506298-2b835587-22ca-44e0-ac61-9a6cec84e454.png">

5.	Select * from tweets_table where recruiter_tweet_location LIKE '%New York%';

Use Case: Enable user to search recruiter location.
Description: Display users the all the recruiter based on a location.
Actor: User
Precondition: Recruiter location must be present.
Steps:
Actor action: User can view recruiters based on a location.
System Responses: Display all the recruiters from the search location.
Alternate Path: No Recruiters are displayed.
Error: Recruiter data currently unavailable.

π j . job_url, t . recruiter_twitter_handle
 σ j . tweet_id = t . tweet_id
  (ρ j job_urls ×
   ρ t tweets_table)
<img width="404" alt="image" src="https://user-images.githubusercontent.com/113727586/201506310-a5dea3e1-1a04-47c3-bbee-081214518772.png">

##Sinchana Kumara

1.Select t.recruiter_twitter_handle,t.tweet_text,t.tweet_date, j.job_url from tweets_table AS t JOIN job_urls AS j ON t.tweet_id = j.tweet_id Order By t.tweet_date desc;

Use Case: Displaying the latest Job data to the users.
Description: User can view latest Job postings.
Actor: User
Precondition: Jobs postings must contain posted date.
Steps:
Actor action: View latest tweets.
System Responses: The list of Jobs ordered by posted_date in Desc are displayed to User.
Alternate Path: There are no latest jobs postings.
Error: No history of jobs  available.

τ t . tweet_date ↓
 π t . recruiter_twitter_handle, t . tweet_text, t . tweet_date, j . job_url
  (ρ t tweets_table ⋈ t . tweet_id = j . tweet_id
   ρ j job_urls)
   
<img width="417" alt="image" src="https://user-images.githubusercontent.com/113727586/201506462-144d327a-db77-4529-b134-d361ec30a43c.png">

   
2. Select Count(application_tweet_id), user_twitter_handle from jobs_applied GROUP BY user_twitter_handle;

Use Case: Display the number of Jobs applied by the user.
Description: User can view the number of Completed job Applications.
Actor: User
Precondition: User must have completed job applications.
Steps:
Actor action: User can view the number of completed Applications.
System Responses: The number of completed job application per user are displayed.
Alternate Path: There user name is displayed with blank count value.
Error: Job applications data not available.

γ user_twitter_handle, COUNT (application_tweet_id) jobs_applied

<img width="420" alt="image" src="https://user-images.githubusercontent.com/113727586/201506474-6de1c132-d5b9-471c-98bb-3aa17b28ff52.png">

3. Select * from tweets_table where tweet_id IN (Select tweet_id from tweet_tags where tags = '#bakingjobs');

Use Case: View the Tweets attached to the tweet with the hashtag “#bakingjobs'”
Description: User views the links related to the hashtag “#bakingjobs'”
Actor: User
Precondition: Tweets must be present with the above hashtag.
Steps:
Actor action: User views all the links for a particular hashtag.
System Responses: The links for the Tweets with hashtags.
Alternate Path: There are no orders made by a user.
Error: No history of orders available.

σ tweet_id IN (π tweet_id
 σ tags = "#bakingjobs" tweet_tags) tweets_table
 
<img width="424" alt="image" src="https://user-images.githubusercontent.com/113727586/201506487-e98df4a5-4eb3-4574-85b7-94df07618c9b.png">

4. Select t.recruiter_twitter_handle, t.tweet_text, t.tweet_date, t.profile_image_url, t.recruiter_tweet_location, j.job_url, s.user_handle from ((tweets_table t INNER JOIN job_urls j ON t.tweet_id = j.tweet_id) INNER JOIN my_saved_applications s ON t.tweet_id = s.job_tweet_id);

Use Case: Display users saved Jobs info such as recruiter , description , recruiter profile image.
Description: Display data for Saved job applications.
Actor: Admin
Precondition: User must have saved job applications.
Steps:
Actor action: User can view his saved Applications.
System Responses: Display all the users save Jobs data.
Alternate Path: No Application data is displayed.
Error: Saved Jobs unavailable.

π t . recruiter_twitter_handle, t . tweet_text, t . tweet_date, t . profile_image_url, t . recruiter_tweet_location, j . job_url, s . user_handle
 (ρ t tweets_table ⋈ t . tweet_id = j . tweet_id

<img width="438" alt="image" src="https://user-images.githubusercontent.com/113727586/201506502-fa5cc6a5-3c26-4908-9edb-bb92370ec227.png">

5. select j.job_url, t.recruiter_twitter_handle from job_urls as j, tweets_table t where j.tweet_id = t.tweet_id;

Use Case: Display all the recruiter application Links.
Description: Display the applications links based on the recruiter.
Actor: User
Precondition: Recruiter must have posted application links.
Steps:
Actor action: User can click and view on links of Applications.
System Responses: Display the list of Links based on the recruiter.
Alternate Path: No Job Application Links are

π j . job_url, t . recruiter_twitter_handle
 σ j . tweet_id = t . tweet_id
  (ρ j job_urls ×
   ρ t tweets_table)

<img width="428" alt="image" src="https://user-images.githubusercontent.com/113727586/201506514-a79f5919-c034-4ee3-8ddf-b4eff98d6592.png">





# Assignment - 3 Gathering, Scraping, Munging and Cleaning Data

## Source of Data:

To obtain relevant and high-quality data, choose the proper data source. For this assignment, we have collected most of the data from Indeed.
Scraping script:
 https://github.com/aiskunks/Jobs_Database/blob/main/One_stop_job/IndeedScraping.ipynb

## Download and reformat the data:

The scraped data was raw data that we audited, cleaned, and validated with completeness. This involved downloading and reformatting the raw data. 
Please find the Github links below:
https://github.com/aiskunks/Jobs_Database/blob/main/One_stop_job/Jobs_All.csv
https://github.com/aiskunks/Jobs_Database/blob/main/One_stop_job/Jobs_Final.ipynb
https://github.com/aiskunks/Jobs_Database/blob/main/One_stop_job/Jobs_All.csv

## Data Validation:

Completeness: refers to the extent to which an entity contains the information needed to describe a real-world object. The presence of null values, which are typically regarded as missing values, in tables in relational database systems can be used to determine how full a table is.

Consistency: The degree to which a set of semantic rules are violated such as a specific data type, an interval for a numerical column, or a set of values for a categorical column.

Accuracy: The correctness of the data and can be measured in two dimensions: syntactic and semantic. Semantic accuracy contrasts a value with its actual representation, while syntactic accuracy compares a value's representation with a domain of definition that corresponds.

## Visualizing Missing Data and Validate data to check missing values (Before Cleaning):

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/205805983-eb5e3077-e242-4788-948b-caef542bd702.png">
Fig 1: Table_Before_Cleaning

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/205806073-08632c95-f50d-4f7c-8e13-e2738631d780.png">
Fig 2: NullValue_count_before

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/205806134-c0354e50-6d1b-4413-b199-ec2a8d1a7191.png">
Fig 3: Heatmap_before

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/205806189-c779dc5a-db9b-4a4b-952b-24fd1b3eec8b.png">
Fig 4: Dendrogram_before

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/205806233-d555b778-b43b-480e-8483-c95f90e21402.png">
Fig 5: Matrix_before

<img width="448" alt="image" src="https://user-images.githubusercontent.com/113729244/205806276-b6c60b3d-b79b-4ebd-af02-c6b809cb0c5a.png">
Fig 6: Bar_graph_before

## Visualizing Missing Data and Validate data to check missing values (After Cleaning):

<img width="444" alt="image" src="https://user-images.githubusercontent.com/113729244/205806725-6d51ffaf-5028-459c-b8ff-ddf4446a3961.png">
Fig 7: Table_after_cleaning

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/205806787-947b755c-9387-4d30-b7e5-21ca414b4a11.png">
Fig 8: NullValue_count_after

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/205806844-d19fe1a7-2f81-4f12-ac14-2d89d01578bc.png">
Fig 9: Heatmap_after

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/205806887-496071fa-f1c3-4896-8719-94e9889c6180.png">
Fig 10: Dendrogram_after

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/205806936-45c3c67c-9206-49de-bdd1-d7619608bfb4.png">
Fig 11: Matrix_after

<img width="468" alt="image" src="https://user-images.githubusercontent.com/113729244/205806965-7f6fb05e-ea5e-4d46-a567-34a090e33753.png">
Fig 12: Bar_graph_after

