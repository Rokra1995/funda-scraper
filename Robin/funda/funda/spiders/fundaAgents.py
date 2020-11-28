import scrapy


class FundaagentsSpider(scrapy.Spider):
    name = 'fundaAgents'
    allowed_domains = ['funda.nl']
    start_urls = ['https://www.funda.nl/en/koop/verkocht/apeldoorn/huis-41029376-distelvlinderlaan-29/']

    def parse(self, response):
        img_urls = pics = response.css('div.object-media-foto > a > img::attr(src)').extract() + response.css('div.object-media-foto > div > img::attr(data-lazy)').extract()

        yield {
            'image_urls': img_urls
        }
