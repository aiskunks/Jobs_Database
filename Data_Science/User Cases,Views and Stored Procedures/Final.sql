ALTER TABLE tasty ADD PRIMARY KEY(Job_id);
ALTER TABLE twitter_urls ADD PRIMARY KEY(Job_id);

-- Views
CREATE OR REPLACE VIEW V_CASE1 AS SELECT City, Company FROM tasty WHERE City LIKE "NEW YORK";
CREATE OR REPLACE VIEW V_CASE3 AS SELECT Company, High_Salary FROM tasty Group By Company Order By High_Salary DESC Limit 3;
CREATE OR REPLACE VIEW V_CASE3 AS SELECT Company, Low_Salary FROM tasty Group By Company Order By Low_Salary  Limit 3;
CREATE OR REPLACE VIEW V_CASE3 AS SELECT Company, Title FROM tasty WHERE Title LIKE "Data Analyst";

-- Adding Index

CREATE INDEX company_index ON tasty(High_Salary);
CREATE INDEX company_index ON twitter_urls(Job_id);

#Stored Procedure
DELIMITER $$
CREATE PROCEDURE Average( IN A_Low INT)
BEGIN
SELECT Company, AVG(Low_Salary) 
FROM tasty
WHERE A_Low= AVG(Low_Salary); 
END;



DELIMITER $$
CREATE PROCEDURE Location_Salary()
BEGIN
SELECT Company, Location, Low_Salary
FROM tasty
WHERE Location LIKE "%Boston%" AND Low_Salary > 90000 ; 
END;

DELIMITER $$
CREATE PROCEDURE Company_names (IN Companies VARCHAR(100))
BEGIN
SELECT Company,Synopsis
FROM tasty
WHERE Company=Companies;
END;


