CREATE TABLE Tweets(
tweet_ID BIGINT PRIMARY KEY NOT NULL UNIQUE, 
tweet_user_ID BIGINT NOT NULL, 
tweet_contents TEXT, 
tweet_date_time DATETIME, 
tweet_location TEXT, 
tweet_rt_count INT, 
tweet_fav_count INT, 
tweet_urls VARCHAR(255), 
keywords VARCHAR(100) DEFAULT NULL, 
source_identifier INT DEFAULT 0);

CREATE TABLE Sources(
source_ID BIGINT PRIMARY KEY NOT NULL UNIQUE, 
source_name VARCHAR(55));

CREATE TABLE Tweet_User(
user_ID BIGINT PRIMARY KEY NOT NULL UNIQUE, 
user_handle VARCHAR(25) NOT NULL UNIQUE, 
user_name VARCHAR(100), 
user_bio VARCHAR(255), 
user_location TEXT, 
user_join_date DATETIME, 
user_fav_count INT, 
user_follower_count INT, 
user_following_count INT, 
twitter_profile_img_url VARCHAR(255));

CREATE TABLE Tweet_Mentions(
mention_row_ID INT PRIMARY KEY NOT NULL UNIQUE,
source_tweet_ID BIGINT,
source_user_ID BIGINT,
mentioned_user VARCHAR(100));

CREATE TABLE Job_Posting(
job_ID BIGINT PRIMARY KEY NOT NULL UNIQUE, 
job_title VARCHAR(255), 
company_ID INT,
posting_datetime DATETIME,
scraped_datetime DATETIME,
application_deadline DATETIME,
salary VARCHAR(155),
job_city VARCHAR(155), 
job_state VARCHAR(155),
posting_url TEXT,
source_identifier INT DEFAULT 0);

CREATE TABLE Company_Team(
company_ID INT PRIMARY KEY NOT NULL UNIQUE, 
company_name VARCHAR(255),
company_headquarters_city VARCHAR(255), 
company_headquarters_state VARCHAR(255), 
league VARCHAR(100), 
league_short VARCHAR(55), 
stadium VARCHAR(55), 
stadium_capacity INT, 
founded_year INT);

CREATE TABLE Job_Requirements(
job_ID BIGINT,
requirements TEXT,
PRIMARY KEY (job_ID, requirements(255)));

#Some Alter Statements from Previous INSERTS Can be ignored:
#ALTER TABLE job_posting
#MODIFY COLUMN salary VARCHAR(155);

#ALTER TABLE job_requirements
#MODIFY COLUMN job_ID BIGINT;

#ALTER TABLE job_posting
#MODIFY COLUMN posting_url TEXT;