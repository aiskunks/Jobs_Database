
DROP DATABASE IF EXISTS `ai_jobs_database`;
CREATE DATABASE `ai_jobs_database`; 

USE `ai_jobs_database`;

SET NAMES utf8mb4;
SET character_set_client = utf8mb4;

/*
Tweet Data Tables
*/

CREATE TABLE `twitter_user` (
`user_id` bigint NOT NULL,
`name` varchar(50) NOT NULL,
`user_name` varchar(50) NOT NULL,
`location` char(50),
`date_joined` date NOT NULL,
PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `job_tweets` (
  `tweet_id` bigint NOT NULL UNIQUE,
  `user_id` bigint NOT NULL,
  `description` varchar(1000) NOT NULL,
  `date_posted` date,
  `like_count` int,
  PRIMARY KEY (`tweet_id`),
  FOREIGN KEY (user_id) REFERENCES twitter_user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `tweet_url` ( 
  `url` varchar(250) NOT NULL UNIQUE, 
`tweet_id` bigint NOT NULL, 
  PRIMARY KEY (`url`,`tweet_id`) 
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `twitter_tag` ( 
 `tag_name` varchar(50) NOT NULL,
 `tweet_id` bigint NOT NULL,  
  PRIMARY KEY (`tag_name`,`tweet_id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci; 


CREATE TABLE `event_tweets` (
  `tweet_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `description` varchar(1000) NOT NULL,
	`date_posted` date,
   `like_count` int,
  PRIMARY KEY (`tweet_id`),
  FOREIGN KEY (user_id) REFERENCES twitter_user(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `derived_tag` (
  `der_tag_name` varchar(50) NOT NULL,
  `tweet_id` BIGINT NOT NULL,
  PRIMARY KEY (`der_tag_name`,`tweet_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


/*
Job Data Tables
*/

CREATE TABLE `company` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `founded_year` int,
  `industry` varchar(200),
  `size` varchar(50),
  `revenue` varchar(50),
  `rating` float,
   PRIMARY KEY(`id`)
);

CREATE TABLE `state_data` (
  `state` varchar(50) NOT NULL,
  `tax_rate` float,
  PRIMARY KEY(`state`)
);

CREATE TABLE `location` (
  `id` bigint NOT NULL UNIQUE AUTO_INCREMENT,
  `city` varchar(50),
  `state` varchar(50) NULL,
  `country` varchar(50),
  `cost_of_living_index` float,
  CONSTRAINT unique_state_city UNIQUE(`city`, `state`),
  PRIMARY KEY(`id`),
  FOREIGN KEY(`state`) REFERENCES state_data(`state`) 
);

CREATE TABLE `jobData` (
  `id` bigint NOT NULL,
  `title` varchar(200),
  `description` text,
  `date_posted` date,
  `location_id` bigint,
  `link` varchar(1500),
  `seniority_level` varchar(50),
  `employmentType` varchar(50),
  `company_id` bigint,
  PRIMARY KEY(`id`),
  FOREIGN KEY (`company_id`) REFERENCES company(`id`),
  FOREIGN KEY (`location_id`) REFERENCES location(`id`)
);

CREATE TABLE `derived_data` (
  `job_id` bigint,
  `category` varchar(50),
  `value` varchar(500),
  FOREIGN KEY(`job_id`) REFERENCES jobData(`id`),
  PRIMARY KEY(`job_id`, `category`, `value`)
);

CREATE TABLE `skill_data` (
  `id` bigint,
  `skill_name` varchar(50),
  PRIMARY KEY(`id`)
);

CREATE TABLE `skill_jobs_data` (
  `skill_id` bigint unique,
  `job_id` bigint unique,
  FOREIGN KEY(`skill_id`) REFERENCES skill_data(`id`),
  FOREIGN KEY(`job_id`) REFERENCES jobData(`id`),
  PRIMARY KEY(`skill_id`,`job_id`)
);

select * from location;




