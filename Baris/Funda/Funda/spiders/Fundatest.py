import scrapy

class FundaSpider(scrapy.Spider):
    name = 'Funda'
    allowed_domains =  ["https://www.funda.nl/"]
    start_urls = ['https://www.funda.nl/koop/verkocht/ijmuiden/huis-41192664-sluisplein-16/']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        yield {
            'House description': response.css('div.object-description-body::text').getall(),
            'House type' : response.xpath('//*[@id="content"]/div/div/div[1]/section[5]/div/dl[2]/dd[1]/text()').get(),
        }