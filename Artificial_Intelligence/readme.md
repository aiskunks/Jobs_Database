# AI Jobs Database

A MySQL Database for AI/ML/DS Jobs contains scraped data like jobs, company profile, cost of living and tax rates from [Linkedin](https://www.linkedin.com/), [Glassdoor](https://www.glassdoor.com/index.htm), [tax rates](https://www.realized1031.com/capital-gains-tax-rate) and [cost of living](https://advisorsmith.com/data/coli/#data).

### Project Features

- Required skillsets for the job. This was extracted from job description using a pretrained Naive Bayes model.
- Displays current openings along with other details – salary, location, experience and desired skills.
- Workplace reviews from glassdoor.
- Database contains cost of living at different cities along with state tax rates from which the savings and in hand salary can be computed.

### Project Execution Stages

- Scraping jobs and company profile Glassdoor, jobs data from Linkedin using Scrapy and Beautiful Soup.
- Fetch data for cost of living and state wise tax rates.
- Creation of Database with ER diagram using Crawford Notation.
- Build a physical MySQL database.
- Normalize database to third Normal Form.
- Data cleaning and feature engineering using pandas, numpy and sklearn.
- Extract skills from job description using Naive Bayes algorithm.
- Load the data into MySQL database.
- Creating visulizations like salaries, job locations and most sought after skills.

### Running Jobs Scraping Bot

Create a new virtual environment at `Artificial_Intelligence/` folder and install the requirements using the following command

```
pip3 install -r requirements.txt
```

Change directory to `AISkunksJobsDatabase/Artificial_Intelligence/JobsBot/JobsBot/JobsBot/spiders`. Update the required search keywords in the file `spiderCoordinator.py`. Run the following command to start scraping

```
scrapy crawl spiderCoordinator
```

### Future Scope

- Creating an automated data pipeline for updating database.
- Performing Comparative analysis of user skillset and working employee skillset and recommending skillset to upscale.
- Creating Alumni database of Northeastern students for a referral.
  \
  &nbsp;

| Team member        | Email                        |
| ------------------ | ---------------------------- |
| Asawari Kadam      | kadam.asa@northeastern.edu   |
| Ashwini Khedkar    | khedkar.as@northeastern.edu  |
| Hariharan Sundaram | sundaram.ha@northeastern.edu |
| Vinay Prabhu       | prabhu.v@northeastern.edu    |
