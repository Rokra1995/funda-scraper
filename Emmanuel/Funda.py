import scrapy



class Funda_Emmanuel_Spider(scrapy.Spider):
    name = "Funda_Emmanuel"
    allowed_domains = ["funda.nl"]
    start_urls = ['https://www.funda.nl/koop/ede/huis-41112604-wilsondreef-20/']
    
    def parse(self, response):
        for funda in response.css('div.object-primary'):
            yield{
                'Postcode': response.css("#content > div > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > h1 > span.object-header__subtitle.fd-color-dark-3::text").extract_first(),
                'Asking_Price': response.css("#content > div > div > div.object-primary > header > div > div > div.object-header__pricing.fd-text-size-l.fd-flex--bp-m.fd-align-items-center > div > strong.object-header__price::text").extract_first(),
                'SQM_Living_Area': response.css("#content > div > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > section > ul > li:nth-child(1) > span.kenmerken-highlighted__value.fd-text--nowrap::text").extract_first(),
                }
