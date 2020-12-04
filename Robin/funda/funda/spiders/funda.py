import scrapy
from datetime import datetime
import re
import os


class FundaSpider(scrapy.Spider):
    name = 'funda'
    allowed_domains = ['funda.nl']
    start_urls = ['https://www.funda.nl/en/koop/gemeente-amsterdam/verkocht/appartement/sorteer-afmelddatum-af/']
   
    def parse(self, response):
        urls = response.css('ol.search-results > li.search-result > div.search-result-main > div.search-result-content >div.search-result-content-inner > div > div.search-result__header-title-col > a::attr(href)').extract()
        count = 0
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, self.parse_details)
            count = count+1
            if count == 5:
                break
        

        next_page_url = response.css('#content > form > div.fd-p-horizontal-none.container.search-main > nav > a::attr(href)').extract_first()
        if len(response.css('#content > form > div.fd-p-horizontal-none.container.search-main.historic > nav >a').extract()) == 2:
            next_page_url = response.css('#content > form > div.fd-p-horizontal-none.container.search-main.historic > nav > a:nth-child(4)::attr(href)').extract_first()
        #for testing purpose only scraping 2 pages
        #next_page_url = '/en/koop/heel-nederland/verkocht/sorteer-afmelddatum-af/p2/'
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(next_page_url, self.parse)

    def parse_details(self,response):
        sales_agents = response.css('div.object-primary > section.object-contact > div > h3.object-contact-aanbieder-name > a::text').extract()
        garden = str(response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(19) > dd:nth-child(4)::text').extract_first()).strip().rstrip("\n").rstrip("\r")
        img_urls = response.css('div.object-media-foto > a > img::attr(src)').extract() + response.css('div.object-media-foto > div > img::attr(data-lazy)').extract()

        yield {
            'zipcode': response.css('#content > div > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > h1 > span.object-header__subtitle.fd-color-dark-3::text').extract_first().strip().rstrip("\n").rstrip("\r").replace(" ","")[:6],
            'sellingDate': datetime.strptime(str(response.css('#content > div > div > div.object-primary > section:nth-child(3) > div > dl > dd:nth-child(4)::text').extract_first()).strip().rstrip("\n").rstrip("\r"), '%B %d, %Y').date(),
            'publicationDate': datetime.strptime(str(response.css('#content > div > div > div.object-primary > section:nth-child(3) > div > dl > dd:nth-child(2)::text').extract_first()).strip().rstrip("\n").rstrip("\r"), '%B %d, %Y').date(),
            'sellingPrice': int(re.findall('\d*\,?\d+',response.css('#content > div > div > div.object-primary > header > div > div > div.object-header__pricing.fd-text-size-l.fd-flex--bp-m.fd-align-items-center > div > strong::text').extract_first().strip().rstrip("\n").rstrip("\r"))[0].replace(",","")),
            'housetype': response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(2)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'categoryobject': response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(4)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'yearofbuilding': response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(6)::text').extract_first().strip().rstrip("\n").rstrip("\r"),
            'garden': garden,
            'garden_binary': 1 if ('garden' in garden) else 0,
            'parcelsurface': int(max(re.findall("\d+", response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd.object-kenmerken-group-list > dl > dd:nth-child(2)::text').extract_first().strip().rstrip("\n").rstrip("\r")))),
            'numberrooms': int(max(re.findall("\d+", response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(11) > dd:nth-child(2)::text').extract_first()))),
            'numberbathrooms': int(max(re.findall("\d+",response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(11) > dd:nth-child(4)::text').extract_first()))),
            'energylabelclass': str(response.css('span.energielabel::text').extract_first()).strip().rstrip("\n").rstrip("\r"),
            'surface': int(max(re.findall("\d+",response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd:nth-child(5)::text').extract_first()))),
            'fulldescription': ''.join(response.css('div.object-description-body *::text').extract()).strip().rstrip("\n").rstrip("\r").replace("  "," ").replace("   "," "),
            'sales_agent': sales_agents[0] if len(sales_agents)>=1 else None,
            'buying_agent': sales_agents[1] if len(sales_agents)==2 else None,
            'url': response,
            'image_urls': img_urls,
        }
