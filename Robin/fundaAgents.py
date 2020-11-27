import scrapy


class FundaagentsSpider(scrapy.Spider):
    name = 'fundaAgents'
    allowed_domains = ['funda.nl']
    start_urls = ['http://funda.nl/']

    def parse(self, response):
        pass
