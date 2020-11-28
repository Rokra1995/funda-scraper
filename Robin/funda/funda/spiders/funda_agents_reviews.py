import scrapy


class FundaAgentsReviewsSpider(scrapy.Spider):
    name = 'funda_agents_reviews'
    allowed_domains = ['funda.nl']
    start_urls = ['http://funda.nl/']

    def parse(self, response):
        pass
