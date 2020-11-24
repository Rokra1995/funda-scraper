import scrapy


class funda_felicia_spider(scrapy.Spider):
    name = 'funda_felicia'
    allowed_domains = ['funda.nl']
    start_urls = ['https://www.funda.nl/koop/heel-nederland/']

    def parse(self, response):
        yield{
            'surface_area_sqm': response.css('#content > form > div.container.search-main > div.search-content #content > form > div.container.search-main > div.search-content > div.search-content-output > ol:nth-child(4) > li:nth-child(1) > div > div.search-result-content > div > div:nth-child(3) > ul > li:nth-child(1) > span:nth-child(2) > span.text::text').getall(),
            #'surface_area_sqm': response.xpath('//*[@id="content"]/form/div[2]/div[3]/span/text').get()
            #'surface_area_sqm': response.css('#content > form > div.container.search-main > <span title="Perceeloppervlakte">163 m²</span>::text').get(),
            #'year_of_construction': response.css('#content > form > div.container.search-main > <span title="Perceeloppervlakte">163 m²</span>::text').get(),
            #'garden': response.css('#content > form > div.container.search-main > <span title="Perceeloppervlakte">163 m²</span>::text').get(),
        }


#content > form > div.container.search-main > div.search-content > div.search-content-output > ol:nth-child(4) > li:nth-child(1) > div > div.search-result-content > div > div:nth-child(3) > ul > li:nth-child(1) > span:nth-child(2)

#content > form > div.container.search-main > div.search-content
#content > form > div.container.search-main > div.search-content > div.search-content-output > ol:nth-child(4) > li:nth-child(1) > div > div.search-result-content > div > div:nth-child(3) > ul > li:nth-child(1) > span:nth-child(2)