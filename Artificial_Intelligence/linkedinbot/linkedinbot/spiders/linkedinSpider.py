import scrapy
from dataclasses import dataclass
from bs4 import BeautifulSoup
import re

@dataclass
class JobData():
    """A class for holding job data content"""
 
    # Attributes Declaration
 
    title: str = ''
    jobId: str = ''
    companyName: str = ''
    location: str = ''
    datePosted: str = ''
    link: str = ''
    description: str = ''
    seniorityLevel: str = ''
    employmentType: str = ''
    jobFunction: str = ''
    industry: str = ''


class LinkedinSpider(scrapy.Spider):
    pageSizeTillNow = 0
    pageSize = 25
    request = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Ai&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=8&pageNum=0&currentJobId=3257884433&start='
    start_urls = [request+str(pageSizeTillNow)]
    shouldEndSearching = False
    name = 'linkedinSpider'

    def tryOptional(self, callableBlock):
        try:
            result = callableBlock()
            return result
        except:
            return None

    def parse(self, response):
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
        
        self.pageSizeTillNow += self.pageSize
        nextPage = self.request+str(self.pageSizeTillNow)
        if (not self.shouldEndSearching):
            yield response.follow(nextPage, callback=self.parse)

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