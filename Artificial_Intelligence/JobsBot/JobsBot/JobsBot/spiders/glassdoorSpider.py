import scrapy
from dataclasses import dataclass
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json

@dataclass
class GlassdoorJobData():
    """A class for holding job data content"""
 
    # Attributes Declaration
    title: str = None
    jobId: str = None
    companyName: str = None
    location: str = None
    datePosted: str = None
    link: str = None
    description: str = None
    salary: str = None
    industry: str = None
    companyRating: float = None
    companyFoundedYear: str = None
    sector: str = None
    size: str = None
    revenue: str = None

# A bot to scrape Glassdoor jobs
class GlassdoorSpider(scrapy.Spider):
    # A counter for iterating through page numbers to follow glassdoor links
    pageNumber = 1
    # A flag which when set to true stops scraping and following links. It is set when either no
    # jobs are returned or when server returns 400 response.
    shouldEndSearching = False
    # Name of the scraping bot
    name = 'glassdoorSpider'
    # Request which is updated based on search term and page number.
    request = 'https://www.glassdoor.com/Job/{{searchTerm}}-jobs-SRCH_KO0,14_IP{{pageNumber}}.htm'

    def __init__(self, *args, **kwargs):
        super(GlassdoorSpider, self).__init__(*args, **kwargs)
        # Takes search term as argument and searches glassdoor with it
        searchTerm = kwargs.get('searchTerm', 'hello world')
        self.request = self.request.replace('{{searchTerm}}', searchTerm.strip().replace(" ", "-"))
        self.start_urls = [self.request.replace('{{pageNumber}}', str(self.pageNumber))]

    # Handles optionals and returns None value when an exception is encountered
    def tryOptional(self, callableBlock):
        try:
            result = callableBlock()
            return result
        except:
            return None

    # A function which is called to follow and open the next page on glassdoor.
    def parse(self, response):
        if response.status == 400:
            self.shouldEndSearching = True
            return None
        soup = BeautifulSoup(response.body, 'lxml')
        # Fetches all jobs listed on a given page
        jobCards = soup.find_all("li", class_="react-job-listing")

        if len(jobCards) == 0:
            self.shouldEndSearching = True
            return None

        # Iterates through job cards and extracts job links from them
        for jobCard in jobCards:
            jobModel = GlassdoorJobData()
            jobModel.link = self.tryOptional(
                lambda: jobCard.find("a", class_="jobLink", href=True)['href']
            ) 
            if(jobModel.link == None):
                continue
            jobModel.link = "https://www.glassdoor.com" + jobModel.link 
            yield scrapy.Request(jobModel.link, callback=self.parseIndividualJobs, cb_kwargs=dict(jobModel=jobModel))
        
        self.pageNumber += 1
        nextPage = self.request.replace("{{pageNumber}}", str(self.pageNumber))
        # Follows and opens the next page after updating url with page number
        if (not self.shouldEndSearching):
            yield response.follow(nextPage, callback=self.parse)

    # Parses individual job page to extract necessary information and maps to the job model
    def parseIndividualJobs(self, response, jobModel):
        jobBannerValid = False
        job = BeautifulSoup(response.body, 'lxml')
        try:
            jobBanner = job.find("div", class_="css-ur1szg e11nt52q0")
            jobBannerValid = True
        except:
            print("[ERROR] Error occurred in function extract_listingBanner")
            return
        
        # Extracts the appcache json from script tag in the retrieved web page
        pattern = re.compile(r'window.appCache')
        scriptText = job.find('script', text=pattern).text
        cacheData = json.loads(scriptText[scriptText.find('{') : scriptText.rfind('}')+1])
        
        if jobBannerValid:
            jobModel.title = self.tryOptional(lambda: jobBanner.find("div", class_="css-17x2pwl e11nt52q6").getText())
            jobModel.salary = self.tryOptional(
                lambda: jobBanner.find("span", class_="small css-10zcshf e1v3ed7e1").getText()
            )
            jobModel.jobId = self.tryOptional(
                lambda: cacheData['initialState']['jlData']['job']['jobReqId']
            )
            jobModel.datePosted = self.tryOptional(
                lambda: cacheData['initialState']['jlData']['header']['posted']
            )
            jobModel.companyName = self.tryOptional(
                lambda: cacheData['initialState']['jlData']['header']['employer']['name']
            )
            jobModel.location = self.tryOptional(
                lambda: job.find("div", class_="css-1v5elnn e11nt52q2").getText()
            )
            jobModel.description = self.tryOptional(
                lambda: job.find("div", class_='desc css-58vpdc ecgq1xb5').getText(' ').strip()
            )
            jobModel.companyFoundedYear = self.tryOptional(
                lambda: cacheData['initialState']['jlData']['overview']['yearFounded']
            )
            jobModel.industry = self.tryOptional (
                lambda: cacheData['initialState']['jlData']['overview']['primaryIndustry']['industryName']
            )
            jobModel.sector = self.tryOptional(
                lambda: cacheData['initialState']['jlData']['overview']['primaryIndustry']['sectorName']
            )
            jobModel.size = self.tryOptional(
                lambda: cacheData['initialState']['jlData']['overview']['size']
            )
            jobModel.revenue = self.tryOptional(
                lambda: cacheData['initialState']['jlData']['overview']['revenue']
            )
            jobModel.companyRating = self.tryOptional(
                lambda: cacheData['initialState']['jlData']['overview']['ratings']['overallRating']
            )
            yield jobModel
