# source ~/VE/bin/activate
# scrapy shell 'https://www.funda.nl/koop/verkocht/amsterdam/huis-41194835-buiksloterdijk-236/
import scrapy


class funda_felicia_spider(scrapy.Spider):
    name = 'funda_felicia'
    allowed_domains = ['funda.nl']
    start_urls = [
        'https://www.funda.nl/koop/verkocht/amsterdam/huis-41194835-buiksloterdijk-236/',
        'https://www.funda.nl/en/koop/verkocht/waalwijk/huis-41100016-poelruitstraat-26/'
    ]

    def parse(self, response):
        for funda in response.css('div.object-primary'):
            yield{
                'surface_area_sqm': funda.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd:nth-child(5)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
                'year_of_construction': funda.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(6)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
                'garden': funda.css('div.object-primary > section:nth-child(7) > div >dl:nth-child(19) > dd:nth-child(4)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            }

'''
notes: for now garden gives an explanation OF the graden of the house, not IF there is a garden. Is that the purpose? Should I dummy code?
'''

# output1: {'surface_area_sqm': '102 m²', 'year_of_construction': '1962', 'garden': 'Back garden and front garden'}
# output2: {'surface_area_sqm': '360 m²', 'year_of_construction': '1984', 'garden': 'Achtertuin'}