# source ~/VE/bin/activate
# scrapy shell https://www.funda.nl/koop/verkocht/amsterdam/huis-41194835-buiksloterdijk-236/
import scrapy


class funda_info_spider(scrapy.Spider):
    name = 'funda_info'
    allowed_domains = ['funda.nl']
    start_urls = [
        'https://www.funda.nl/koop/verkocht/amsterdam/huis-41194835-buiksloterdijk-236/',
        'https://www.funda.nl/en/koop/verkocht/waalwijk/huis-41100016-poelruitstraat-26/',
    ]

    def parse(self, response):
        for funda in response.css('div.object-primary'):
            yield{
                'surface_area_sqm': response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd:nth-child(5)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
                'year_of_construction': response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(6)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
                'description_garden': response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(19) > dd:nth-child(4)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            }

'''
output1: {'surface_area_sqm': '102 m²', 'year_of_construction': '1962', 'garden': 'Back garden and front garden'}
output2: {'surface_area_sqm': '360 m²', 'year_of_construction': '1984', 'garden': 'Achtertuin'}
'''


# scrapy shell https://www.funda.nl/makelaars/kantoor/alkmaar/12285-makelaarsland/
class broker_info_spider(scrapy.Spider):
    name = 'broker'
    allowed_domains = ['funda.nl']
    start_urls = [
        'https://www.funda.nl/makelaars/kantoor/alkmaar/12285-makelaarsland/',
        'https://www.funda.nl/makelaars/kantoor/waalwijk/11082-van-de-zande-makelaardij-waalwijk/', 
    ]

    def parse(self, response):        
        for funda in response.css('#content'):
            yield{
                'name_broker': response.css('div.container.makelaars-container > div:nth-child(2) > h1::text').extract_first(), # =response.css('h1::text').extract_first(),
                'postcode_broker': response.css('div.makelaars-contact > div > div.makelaars-contact-container > div:nth-child(1) > div.makelaars-contact-item.makelaars-contact-address > p > span:nth-child(3)::text').extract_first(),
                'description_broker': response.css('#content > div > div.container > div.makelaars-kantoor-details > section.makelaars-about > div > div > p:nth-child(2)::text').extract_first().replace(u'\xa0', u' ').replace(u'\r', u' ').replace(u'\n', u' '),
                'score_broker': float(''.join(response.css('#content > div > section.makelaars-reviews > div > div > div:nth-child(1) > span *::text').extract()).replace(',','.')),
                'number_reviews_broker': float(''.join(response.css('#content > div > section.makelaars-reviews > div > div > div:nth-child(1) > a > span *::text').extract())),
                'number_houses_for_sale_offered': float(''.join((response.css('div.makelaars-stats > div:nth-child(1) > div > div:nth-child(2) > div.makelaars-stats-number::text').extract()))),
                'number_houses_sold_last_12_months': float(''.join(response.css('div.makelaars-stats > div:nth-child(2) > div > div:nth-child(2) > div.makelaars-stats-number::text').extract())),
            } 

# *:: = select everything that is in the child = output list
# ''.join(outputlist) = string generation
# float(''join(outputlist)) to be able to do calculations 
# write replace function . to , to be able to convert string to float! 
 
''''    
output1: 
'name_broker': 'Van de Zande Makelaardij Waalwijk', 
'postcode_broker': '5142 CD', 
'description_broker': 'Van de Zande Makelaardij is al ruim 60 jaar actief bij de  begeleiding van transacties in de wereld van onroerende zaken. Onze  werkzaamheden omvatten zowel het taxeren van woningen en  bedrijfsobjecten, de begeleiding van aan- en verkoop van bestaande  en nieuwbouw woningen alsmede de begeleiding van transacties van  bedrijfsmatige onroerende zaken.', 
'score_broker': 9.1, 
'number_reviews_broker': 214.0, 
'number_houses_for_sale_offered': 67.0, 
'number_houses_sold_last_12_months': 130.0


output2: 
'name_broker': 'Makelaarsland', 
'postcode_broker': '1821 BS', 
'description_broker': 'Wij zijn Makelaarsland, en wij staan naast je als je dat nodig  hebt en achter je als je zelf het heft in handen neemt. Wij helpen  en ontzorgen. Wij zorgen ervoor dat je makkelijk, snel en effectief  je huis verkoopt óf een ander aankoopt. Met ervaring,  logica, de laatste techniek van vandaag en pasklare oplossingen en  gaan altijd voor het maximaal haalbare resultaat. Gegarandeerd. We  spannen ons voor ieder huis even hard in.  We hebben een vast  tarief en maken heldere afspraken. En dat doen we allemaal op een  nuchtere, open en eerlijke manier. Wij zijn Makelaarsland, we  geloven niet in mooie praatjes en maken waar wat we beloven.', 
'score_broker': 8.8, 
'number_reviews_broker': 6.693, 
'number_houses_for_sale_offered': 608.0, 
'number_houses_sold_last_12_months': 2733.0

'''

