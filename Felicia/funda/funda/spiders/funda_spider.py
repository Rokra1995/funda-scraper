# source ~/VE/bin/activate
# scrapy shell https://www.funda.nl/koop/verkocht/amsterdam/huis-41194835-buiksloterdijk-236/
import scrapy
import unicodedata

class funda_info_spider(scrapy.Spider):
    name = 'funda_info'
    allowed_domains = ['funda.nl']
    start_urls = [
        'https://www.funda.nl/koop/verkocht/amsterdam/huis-41194835-buiksloterdijk-236/',
        'https://www.funda.nl/en/koop/verkocht/waalwijk/huis-41100016-poelruitstraat-26/',
    ]

    def parse(self, response):
        for funda in response.css('div.object-primary'):
            item = {
                'surface_area_sqm': response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd:nth-child(5)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
                'year_of_construction': response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(6)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
                'description_garden': response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(19) > dd:nth-child(4)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            }
            yield item

# scrapy shell https://www.funda.nl/makelaars/kantoor/alkmaar/12285-makelaarsland/
# scrapy shell https://www.funda.nl/makelaars/heel-nederland/verkoop/
class broker_info_spider(scrapy.Spider):
    name = 'broker'
    allowed_domains = ['funda.nl']
    start_urls = [
        'https://www.funda.nl/makelaars/heel-nederland/verkoop/',
    ]
    
    def parse(self, response):
        urls = response.css('ol.search-results.fd-p-horizontal > li.makelaars-result-item > div > a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, self.parse_details,
            )
            
        #go to the next page and scrape the broker details 
        next_page_url = response.css('#content > form > div.container.search-main.makelaar-search-results-main > nav > a::attr(href)').extract_first()
        #make sure spider clicks on 'next' page instead of previous page as from the 2nd page on there are 2 'a' objects 
        if len(response.css('#content > form > div.container.search-main.makelaar-search-results-main > nav > a').extract()) > 1:
            next_page_url = response.css('#content > form > div.container.search-main.makelaar-search-results-main > nav > a:nth-child(4)::attr(href)').extract_first()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(next_page_url, self.parse)
        
    def int_check(self, number):
        if number != None and number.isnumeric() == True:
            return int(number)
        else:
            return "Missing" 
            
    def catch_missing(self, text):
        if text == None:
            return "Missing value"
        elif len(text) < 1:
            return "No entry"
        else:
            return text

    def parse_details(self, response):        
        for funda in response.css('#content'):
            yield{
                'name_broker': self.catch_missing(response.css('div.container.makelaars-container > div:nth-child(2) > h1::text').extract_first()),
                'zipcode_broker': self.catch_missing(response.css('div.makelaars-contact > div > div.makelaars-contact-container > div:nth-child(1) > div.makelaars-contact-item.makelaars-contact-address > p > span:nth-child(3)::text').extract_first()),
                'description_broker': self.catch_missing(unicodedata.normalize('NFKC', ''.join(response.css('#content > div > div.container > div.makelaars-kantoor-details > section.makelaars-about > div > div > p::text').extract()))).replace(u'\r', u' ').replace(u'\n', u''),
                'number_reviews_broker': self.int_check(response.css('#content > div > section.makelaars-reviews > div > div > div:nth-child(1) > a > span *::text').extract_first()),
                'number_houses_for_sale_offered': self.int_check(response.css('div.makelaars-stats > div:nth-child(1) > div > div:nth-child(2) > div.makelaars-stats-number::text').extract_first()),
                'number_houses_sold_last_12_months': self.int_check(response.css('div.makelaars-stats > div:nth-child(2) > div > div:nth-child(2) > div.makelaars-stats-number::text').extract_first()),
                'url': response.url
            }
           
# *:: = select everything that is in the child = output list
# ''.join(outputlist) = string generation
# float(''join(outputlist)) to be able to do calculations 
# write replace function . to , to be able to convert string to float! 