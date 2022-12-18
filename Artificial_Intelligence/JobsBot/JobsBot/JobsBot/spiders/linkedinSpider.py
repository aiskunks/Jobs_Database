import scrapy
from dataclasses import dataclass
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

@dataclass
class JobData():
    """A class for holding job data content"""
    # Attributes Declaration
    title: str = None
    jobId: str = None
    companyName: str = None
    location: str = None
    datePosted: str = None
    link: str = None
    description: str = None
    seniorityLevel: str = None
    employmentType: str = None
    jobFunction: str = None
    industry: str = None

# A bot to scrape Linkedin jobs
class LinkedinSpider(scrapy.Spider):
    # A scraped jobs offset to continue scraping
    pageSizeTillNow = 0
    # Indicates the number of jobs present on each page
    pageSize = 25
    # A flag to control and stop searching process
    shouldEndSearching = False
    # Name of the spider 
    name = 'linkedinSpider'
    # Request which can be updated with search term and jobs offset
    request = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={{searchTerm}}&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=8&pageNum=0&currentJobId=3257884433&start='

    def __init__(self, *args, **kwargs):
        super(LinkedinSpider, self).__init__(*args, **kwargs)
        # Receives the search term as a parameter and percentage encodes it
        encodedSearchTerm = quote(kwargs.get('searchTerm', 'hello world'))
        # Updates the request with search term and jobs offset
        self.request = self.request.replace('{{searchTerm}}', encodedSearchTerm)
        self.start_urls = [self.request+str(self.pageSizeTillNow)]

    # Handles exceptions gracefully. It returns None type on exception.
    def tryOptional(self, callableBlock):
        try:
            result = callableBlock()
            return result
        except:
            return None

    # Parses each linkedin page and follows the job links and consecutive page links with offset
    def parse(self, response):
        # Stops searching when server returns 400 response
        if response.status == 400:
            self.shouldEndSearching = True
            return None
        soup = BeautifulSoup(response.body, 'lxml')
        for job in soup.findAll('div', class_='job-search-card'):
            jobModel = JobData()
            jobModel.jobId = self.tryOptional(lambda: (job.attrs['data-entity-urn'].split('jobPosting:')[1]))
            jobModel.title = self.tryOptional(lambda: job.find('h3').text.strip())
            jobModel.companyName = self.tryOptional(lambda: job.find(class_='base-search-card__subtitle').text.strip())
            jobModel.location = self.tryOptional(lambda: job.find(class_="job-search-card__location").text.strip())
            jobModel.datePosted = self.tryOptional(lambda: job.find('time', class_='job-search-card__listdate').attrs['datetime'])
            jobModel.link = self.tryOptional(lambda: job.find('a').attrs['href'])
            yield scrapy.Request(jobModel.link, callback=self.parseIndividualJobs, cb_kwargs=dict(jobModel=jobModel))
        # Fetched jobs offset to update url and move to next page
        self.pageSizeTillNow += self.pageSize
        nextPage = self.request+str(self.pageSizeTillNow)
        if (not self.shouldEndSearching):
            yield response.follow(nextPage, callback=self.parse)

    # Parses individual job pages and maps to the jobModel
    def parseIndividualJobs(self, response, jobModel):
        job = BeautifulSoup(response.body, 'lxml')
        jobModel.description = self.tryOptional(lambda: job.find('div', class_='description__text').getText(' ').strip())
        jobModel.seniorityLevel = self.tryOptional(
            lambda: job.find(text=re.compile('Seniority level')).parent.parent.find('span').text.strip()
            )
        jobModel.employmentType = self.tryOptional(
            lambda: job.find(text=re.compile('Employment type')).parent.parent.find('span').text.strip()
            )
        jobModel.jobFunction = self.tryOptional(
            lambda: job.find(text=re.compile('Job function')).parent.parent.find('span').text.strip()
            )
        jobModel.industry = self.tryOptional(
            lambda: job.find(text=re.compile('Industries')).parent.parent.find('span').text.strip()
            )
        yield jobModel


