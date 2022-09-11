-------------creating table for Companies----------------------
Drop table comp_details

Create Table Comp_details(
    CompID INTEGER PRIMARY KEY NOT NULL,
	company nvarchar(MAX),
	location_job nvarchar(MAX),
	domain nvarchar(MAX),
);

Select * from Comp_details

-------------creating table for JOBS----------------------

Drop table Job_details

Create Table Job_details(
    JobID INTEGER PRIMARY KEY NOT NULL,
	CompID INTEGER references Comp_details(CompID),
	title nvarchar(max),
	summary nvarchar (max),
	job_desc nvarchar(max),
	salary nvarchar(max),
	job_type nvarchar(max),
);

Alter Table Job_details
	Add FOREIGN KEY (CompID) REFERENCES Comp_details(CompID);

Select * from Job_details

--1. Stored procedure for companies with analyst postions.

drop procedure analyst

create procedure analyst 
as
select *  
from Job_details
where title like '%Analyst%';
GO

EXEC analyst

--2. Jobs that are offered on contract basis

create procedure Contracttype as
select cd.company, cd.location_job, jb.title, jb.salary, jb.job_type from Comp_details as cd
inner join Job_details as jb on
cd.CompID=jb.CompID where  jb.job_type='Contract';
Go

exec Contracttype

drop view Type_job

--3. View for jobs that are offered for full time.

create view fullTime(job_type,jobID) 
AS SELECT job_type,COUNT(*)
FROM Job_details
WHERE job_type like '%Full time%' GROUP BY job_type;

select * from fullTime;


SELECT * FROM C.CompId CID
LEFT OUTER JOIN C.location_job CLOC ON CID
FROM Comp_details AS C, Job_details AS J
INNER JOIN Comp_details ON C.CompID=J.CompID;

--4. Jobs that are offer intermediate level of salary (around $50000)?

drop procedure more_salary

create procedure more_salary 
as
select cd.company, cd.location_job, jb.title, jb.salary, jb.job_type from Comp_details as cd
inner join Job_details as jb on
cd.CompID=jb.CompID where  jb.salary like '$5%';
go

EXEC more_salary

--5. view for Jobs in around boston area.

create view Boston_Strong as
select * from Comp_details as cd
where cd.location_job='Boston, MA';

select * from Boston_Strong