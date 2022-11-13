
DROP DATABASE IF EXISTS `ai_jobs_database`;
CREATE DATABASE `ai_jobs_database`; 

USE `ai_jobs_database`;

SET NAMES utf8 ;
SET character_set_client = utf8mb4 ;

CREATE TABLE `twitter_user` (
`user_id` smallint(10) NOT NULL,
`name` varchar(50) NOT NULL,
`user_name` varchar(50) NOT NULL,
`location` char(50),
`date_joined` date NOT NULL,
PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE `job_tweets` (
  `tweet_id` bigint(50) NOT NULL UNIQUE,
  `description` varchar(1000) NOT NULL,
  `date_posted` date,
  `like_count` int,
  PRIMARY KEY (`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE `tweet_url` ( 
  `url` varchar(250) NOT NULL UNIQUE, 
`tweet_id` bigint(20) NOT NULL, 
  PRIMARY KEY (`url`,`tweet_id`) 
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;  
ALTER TABLE `derived_tag` ADD CONSTRAINT `tweets_fk1` FOREIGN KEY (`tweet_id`) REFERENCES `job_tweets`(tweet_id);  
ALTER TABLE `derived_tag` ADD CONSTRAINT `tweets_fk2` FOREIGN KEY (`tweet_id`) REFERENCES `event_tweets`(tweet_id); 



CREATE TABLE `twitter_tag` ( 
  `tag_name` varchar(50) NOT NULL, 
 `tweet_id` bigint(20) NOT NULL,  
  PRIMARY KEY (`tag_name`,`tweet_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci; 
ALTER TABLE `derived_tag` ADD CONSTRAINT `tweets_fk1` FOREIGN KEY (`tweet_id`) REFERENCES `job_tweets`(tweet_id);  
ALTER TABLE `derived_tag` ADD CONSTRAINT `tweets_fk2` FOREIGN KEY (`tweet_id`) REFERENCES `event_tweets`(tweet_id); 


CREATE TABLE `event_tweets` (
  `tweet_id` bigint(50) NOT NULL,
  `description` varchar(1000) NOT NULL,
   `date_posted` date,
  PRIMARY KEY (`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE `derived_tag` (
  `der_tag_name` varchar(50) NOT NULL,
  `tweet_id` BIGINT(10) NOT NULL,
  PRIMARY KEY (`der_tag_name`,`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
ALTER TABLE `derived_tag` ADD CONSTRAINT `tweets_fk1` FOREIGN KEY (`tweet_id`) REFERENCES `job_tweets`(tweet_id); 
ALTER TABLE `derived_tag` ADD CONSTRAINT `tweets_fk2` FOREIGN KEY (`tweet_id`) REFERENCES `event_tweets`(tweet_id); 


