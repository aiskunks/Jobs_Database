USE ai_jobs_database;

SELECT title, description, date_posted, link
FROM JobData WHERE description LIKE '%H1B%' AND company_id IN (SELECT id FROM
Company WHERE name='Johnson & Johnson');