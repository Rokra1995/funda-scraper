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
                'surface_area_sqm': funda.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd:nth-child(5)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
                'year_of_construction': funda.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(6)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
                'description_garden': funda.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(19) > dd:nth-child(4)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
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
        for funda in response.css('div.container.makelaars-container'):
            yield{
                'name_broker': funda.css('div.container.makelaars-container > div:nth-child(2) > h1::text').extract_first(), # =response.css('h1::text').extract_first(),
                'description_broker': funda.css('#content > div > div.container > div.makelaars-kantoor-details > section.makelaars-about > div > div > p:nth-child(2)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            }
        
        for funda in response.css('#content'):
            yield{
                'score_broker': ''.join(funda.css('#content > div > section.makelaars-reviews > div > div > div:nth-child(1) > span *::text').extract()),
                'number_reviews_broker': ''.join(funda.css('#content > div > section.makelaars-reviews > div > div > div:nth-child(1) > a > span *::text').extract()),
            } 
            
''''    
output1: {'name_broker': 'Van de Zande Makelaardij Waalwijk', 
'description_broker': 'Van de Zande Makelaardij is al ruim 60 jaar actief bij de\r\nbegeleiding van transacties in de wereld van onroerende zaken. Onze\r\nwerkzaamheden omvatten zowel het taxeren van woningen en\r\nbedrijfsobjecten, de begeleiding van aan- en verkoop van bestaande\r\nen nieuwbouw woningen alsmede de begeleiding van transacties van\r\nbedrijfsmatige onroerende zaken.'}
{'score_broker': '9,1', 'number_reviews_broker': '214'}
                
output2: {'name_broker': 'Makelaarsland', 
'description_broker': 'Wij zijn Makelaarsland, en wij staan naast je als je dat nodig\r\nhebt en achter je als je zelf het heft in handen neemt. Wij helpen\r\nen ontzorgen. Wij zorgen ervoor dat je makkelijk, snel en effectief\r\nje huis verkoopt óf een ander aankoopt. Met ervaring,\r\nlogica, de laatste techniek van vandaag en pasklare oplossingen en\r\ngaan altijd voor het maximaal haalbare resultaat. Gegarandeerd. We\r\nspannen ons voor ieder huis even hard in.\xa0 We hebben een vast\r\ntarief en maken heldere afspraken. En dat doen we allemaal op een\r\nnuchtere, open en eerlijke manier. Wij zijn Makelaarsland, we\r\ngeloven niet in mooie praatjes en maken waar wat we beloven.'}
{'score_broker': '8,8', 'number_reviews_broker': '6.690'}

'''
