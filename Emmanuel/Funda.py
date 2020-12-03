import scrapy



class QuoteSpide(scrapy.Spider):
    name = "Funda"
    allowed_domains = ["funda.nl"]
    start_urls = ['https://www.funda.nl/koop/ede/huis-41112604-wilsondreef-20/']
    
    def parse(self, response):
        self.log('I just visited: '+ response.url)
        yield {
                'Postcode': response.css("#content > div > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > h1 > span.object-header__subtitle.fd-color-dark-3::text").extract_first(),
                'Asking_Price': response.css("#content > div > div > div.object-primary > header > div > div > div.object-header__pricing.fd-text-size-l.fd-flex--bp-m.fd-align-items-center > div > strong.object-header__price::text").extract_first(),
                'SQM_Living_Area': response.css("#content > div > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > section > ul > li:nth-child(1) > span.kenmerken-highlighted__value.fd-text--nowrap::text").extract_first(),
                'Name Broker': response.css("#content > div > div > div.object-secondary > section > div > h3 > a::text").extract_first()
                'Asking_Price_M2': response.xpath("//html/body/main/div/div/div[1]/section[4]/div/dl[1]/dd[2]/text()").extract_first().strip()
                'Services': response.xpath("/html/body/main/div/div/div[1]/section[4]/div/dl[4]/dd[5]/text()").extract_first().strip()
        }
