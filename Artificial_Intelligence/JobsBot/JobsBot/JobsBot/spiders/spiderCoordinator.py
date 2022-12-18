from JobsBot.spiders.linkedinSpider import LinkedinSpider
from JobsBot.spiders.glassdoorSpider import GlassdoorSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


linkedinSearchKeywords = ['Data Scientist', 'Data Analyst']
glassdoorSearchKeywords = ['Data Scientist', 'artificial intelligence engineer']

# Creates and triggers the crawl process by building multiple spiders for each keyword and 
# runs them concurrently. 
def startCrawling():
    process = CrawlerProcess(get_project_settings())
    for searchKeyword in linkedinSearchKeywords:
        keywords = {'searchTerm': searchKeyword}
        process.crawl(LinkedinSpider, **keywords)
    for searchKeyword in glassdoorSearchKeywords:
        keywords = {'searchTerm': searchKeyword}
        process.crawl(GlassdoorSpider, **keywords)
    process.start(stop_after_crawl=False)

startCrawling()