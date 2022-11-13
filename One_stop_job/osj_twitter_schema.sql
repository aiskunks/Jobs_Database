CREATE DATABASE TWITTER_SCHEMA;
USE TWITTER_SCHEMA;

CREATE TABLE `osj_account` (
  `twitter_handle` varchar(256) NOT NULL,
  `password` varchar(256) DEFAULT NULL,
  `role` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`twitter_handle`)
);

CREATE TABLE `osj_users` (
  `twitter_handle` varchar(256) NOT NULL,
  `screen_name` varchar(256) DEFAULT NULL,
  `description` varchar(1024) DEFAULT NULL,
  `location` varchar(128) DEFAULT NULL,
  `joined_date` timestamp NULL DEFAULT NULL,
  `user_id` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`twitter_handle`),
  CONSTRAINT `USER_CONSTRAINT` FOREIGN KEY (`twitter_handle`) REFERENCES `osj_account` (`twitter_handle`)
);

CREATE TABLE `tweets_table` (
  `tweet_id` bigint NOT NULL,
  `recruiter_twitter_handle` varchar(64) DEFAULT NULL,
  `tweet_text` varchar(1000) DEFAULT NULL,
  `tweet_date` timestamp NULL DEFAULT NULL,
  `profile_image_url` varchar(256) DEFAULT NULL,
  `recruiter_tweet_location` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`tweet_id`)
);

CREATE TABLE `tweet_tags` (
  `tweet_id` bigint NOT NULL,
  `tags` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`tweet_id`),
  CONSTRAINT `USER_TAG_CONSTRAINT` FOREIGN KEY (`tweet_id`) REFERENCES `tweets_table` (`tweet_id`)
);

CREATE TABLE `job_urls` (
  `tweet_id` bigint DEFAULT NULL,
  `job_url` varchar(256) NOT NULL,
  PRIMARY KEY (`job_url`),
  KEY `TWEET_URL_CONSTRAINT` (`tweet_id`),
  CONSTRAINT `TWEET_URL_CONSTRAINT` FOREIGN KEY (`tweet_id`) REFERENCES `tweets_table` (`tweet_id`)
);


CREATE TABLE `my_saved_applications` (
  `job_tweet_id` bigint NOT NULL,
  `recruiter_twitter_handle` varchar(256) DEFAULT NULL,
  `user_handle` varchar(256) NOT NULL,
  `post_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`job_tweet_id`,`user_handle`),
  KEY `SAVED_URL_CONSTRAINT` (`user_handle`),
  CONSTRAINT `JOB_TWEET_ID_CONSTRAINT` FOREIGN KEY (`job_tweet_id`) REFERENCES `tweets_table` (`tweet_id`)
);

CREATE TABLE `jobs_applied` (
  `application_tweet_id` bigint NOT NULL,
  `job_url` varchar(256) DEFAULT NULL,
  `user_twitter_handle` varchar(256) DEFAULT NULL,
  `applied_tweet_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`application_tweet_id`),
  KEY `JOBS_APPLIED_CONSTRAINT` (`job_url`),
  CONSTRAINT `JOBS_APPLIED_CONSTRAINT` FOREIGN KEY (`job_url`) REFERENCES `job_urls` (`job_url`)
);
