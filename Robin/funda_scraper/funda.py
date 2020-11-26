import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime
import re

def make_dict(key_list, val_list):
    cleaned_key_list = []
    cleaned_val_list = []
    for i in range(len(key_list)):
        element = key_list[i].strip().rstrip("\n").rstrip("\r")
        cleaned_key_list.append(element)
    for i in range(len(val_list)):
        element = val_list[i].strip().rstrip("\n").rstrip("\r")
        cleaned_val_list.append(element)
    cleaned_val_list.pop(4)
    cleaned_val_list.pop(5)
    cleaned_val_list.pop(10)
    cleaned_key_list.pop(5)
    cleaned_key_list.pop(12)
    cleaned_val_list.pop(24)
    cleaned_val_list.pop(24)
    return dict(zip(cleaned_key_list,cleaned_val_list))

class FundaSpider(scrapy.Spider):
    name = 'funda'
    allowed_domains = ['funda.nl']

    custom_settings = {
        'SPLASH_URL': 'http://localhost:8050',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    }

    #start_urls = ['http://funda.nl']
    #start_urls = ['https://www.funda.nl/en/koop/verkocht/veghel/appartement-41032045-zwijsenhof-106/']
    #start_urls = ['https://www.funda.nl/en/koop/heel-nederland/verkocht/']
    start_urls = ['https://www.funda.nl/en/koop/gemeente-amsterdam/verkocht/appartement/sorteer-afmelddatum-af/']
    

    def parse(self, response):
        urls = response.css('ol.search-results > li.search-result > div.search-result-main > div.search-result-content >div.search-result-content-inner > div > div.search-result__header-title-col > a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, self.parse_details,
            )

    def parse_details(self,response):
        kenmerken_dict = make_dict(response.css('dt::text').extract(),response.css('dd::text').extract())
        object_info = response.css('div.object-primary')
        yield {
            'zipcode': response.css('#content > div > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > h1 > span.object-header__subtitle.fd-color-dark-3::text').extract_first().strip().rstrip("\n").rstrip("\r").replace(" ","")[:6],
            'sellingDate': datetime.strptime(response.css('#content > div > div > div.object-primary > section:nth-child(3) > div > dl > dd:nth-child(4)::text').extract_first().strip().rstrip("\n").rstrip("\r"), '%B %d, %Y').date(),
            'publicationDate': datetime.strptime(response.css('#content > div > div > div.object-primary > section:nth-child(3) > div > dl > dd:nth-child(2)::text').extract_first().strip().rstrip("\n").rstrip("\r"), '%B %d, %Y').date(),
            'sellingPrice': int(re.findall('\d*\,?\d+',response.css('#content > div > div > div.object-primary > header > div > div > div.object-header__pricing.fd-text-size-l.fd-flex--bp-m.fd-align-items-center > div > strong::text').extract_first().strip().rstrip("\n").rstrip("\r"))[0].replace(",","")),
            'housetype': response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(2)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'categoryobject': response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(4)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'yearofbuilding': response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(6)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'garden': response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(19) > dd:nth-child(4)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'garden_binary': 1 if ('garden' in response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(19) > dd:nth-child(4)::text').extract_first().strip().rstrip("\n").rstrip("\r")) else 0,
            'parcelsurface': int(max(re.findall("\d+", response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd.object-kenmerken-group-list > dl > dd:nth-child(2)::text').extract_first().strip().rstrip("\n").rstrip("\r")))),
            'numberrooms': int(max(re.findall("\d+", response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(11) > dd:nth-child(2)::text').extract_first()))),
            'numberbathrooms': int(max(re.findall("\d+",response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(11) > dd:nth-child(4)::text').extract_first()))),
            'energylabelclass': response.css('span.energielabel::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'surface': int(max(re.findall("\d+",response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd:nth-child(5)::text').extract_first()))),
            'fulldescription': ''.join(response.css('div.object-description-body *::text').extract()).strip().rstrip("\n").rstrip("\r").replace("  "," ").replace("   "," "),
            'url': response,
        }


'''
'publicationDate': kenmerken_dict['Listed since'],
'number_rooms': kenmerken_dict['Number of rooms'],
'number_bathrooms': kenmerken_dict['Number of bath rooms'],
'''
