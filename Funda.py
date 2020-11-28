import scrapy

class FundaSpider(scrapy.Spider):
    name = 'Funda'
    allowed_domains =  ['funda.nl']
    start_urls = ['https://www.funda.nl/koop/heel-nederland/verkocht/sorteer-afmelddatum-af/']

    def parse(self, response):
        urls = response.css('div.search-result__header-title-col > a::attr(href)').getall()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)

        # follow pagination link
        next_page_url = response.xpath('//*[@id="content"]/form/div[2]/nav/a/@href').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        yield {
            'zipcode': response.css('#content > div > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > h1 > span.object-header__subtitle.fd-color-dark-3::text').getall(),
            'House description': response.css('div.object-description-body::text').getall(),
            'House type' : response.xpath('//*[@id="content"]/div/div/div[1]/section[5]/div/dl[2]/dd[1]/text()').get(),
            'surface_area_sqm': response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd:nth-child(5)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'year_of_construction': response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(6)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'garden': response.css('div.object-primary > section:nth-child(7) > div >dl:nth-child(19) > dd:nth-child(4)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'Asking_Price': response.css("#content > div > div > div.object-primary > header > div > div > div.object-header__pricing.fd-text-size-l.fd-flex--bp-m.fd-align-items-center > div > strong.object-header__price::text").extract_first(),
            'SQM_Living_Area': response.css("#content > div > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > section > ul > li:nth-child(1) > span.kenmerken-highlighted__value.fd-text--nowrap::text").extract_first(),
            }