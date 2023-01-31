ALTER TABLE job_posting
MODIFY COLUMN salary VARCHAR(155);

ALTER TABLE job_requirements
MODIFY COLUMN job_ID BIGINT;

ALTER TABLE job_posting
MODIFY COLUMN posting_url TEXT;

ALTER TABLE job_requirements
ADD PRIMARY KEY(job_ID, requirements(255));