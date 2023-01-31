CREATE VIEW NHL_Analysts AS
SELECT c.company_name, p.job_title, c.league_short, p.job_city, p.job_state
FROM job_posting p
JOIN company_team c
ON p.company_ID = c.company_ID
WHERE p.job_title LIKE "%analyst%" and c.league_short = "NHL" OR c.company_name = 'National Hockey League';

CREATE VIEW MA_job_postings AS
SELECT p.job_ID, p.job_title, p.job_city, p.job_state, r.requirements
FROM job_posting p
JOIN job_requirements r
ON p.job_ID = r.job_ID
WHERE p.job_state LIKE "%MA";

CREATE VIEW league_listings AS
SELECT  c.league_short, COUNT(p.job_ID) as league_postings
FROM job_posting p
JOIN company_team c
ON p.company_ID = c.company_ID
GROUP BY c.league_short
ORDER BY league_postings DESC;

CREATE VIEW remote_non_league AS
SELECT p.job_ID, p.job_title, p.scraped_datetime, p.job_city, p.posting_url, c.company_ID, c.company_name
FROM job_posting p
JOIN company_team c
ON p.company_ID = c.company_ID
WHERE c.league IS NULL AND (p.job_city LIKE "%remote%" OR p.job_state LIKE "%remote%");

CREATE VIEW spring_jobs AS
SELECT c.company_name, p.job_title, c.league_short, p.posting_url
FROM job_posting p
JOIN company_team c
ON p.company_ID = c.company_ID
WHERE p.job_title LIKE "%Spring%";

SELECT * FROM sources;