import scrapy
from datetime import datetime
import re
import os


# This class contains are spide that scrapes the housing informationon sold houses on the funda website
class FundaSpider(scrapy.Spider):
    name = 'funda_final'
    allowed_domains = ['funda.nl']
    start_urls = ['https://www.funda.nl/en/koop/gemeente-amsterdam/verkocht/appartement/sorteer-afmelddatum-af/']
   
    def parse(self, response):
        #extracting all the urls from the houselistings
        urls = response.css('ol.search-results > li.search-result > div.search-result-main > div.search-result-content >div.search-result-content-inner > div > div.search-result__header-title-col > a::attr(href)').extract()
        count = 0
        #parse housedetail of each house on the current houselistingspage
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, self.parse_details)
            #This counter is included to only scrape 5 houses of each page. Will be removed for the final scrape run
            count = count+1
            if count == 5:
                break  

        #the link to the next listings page will be defined here
        next_page_url = response.css('#content > form > div.fd-p-horizontal-none.container.search-main > nav > a::attr(href)').extract_first()
        #since the location for the next_page button changes after the first lisitngs page we use this if to determine the right link
        if len(response.css('#content > form > div.fd-p-horizontal-none.container.search-main.historic > nav >a').extract()) == 2:
            next_page_url = response.css('#content > form > div.fd-p-horizontal-none.container.search-main.historic > nav > a:nth-child(4)::attr(href)').extract_first()
        
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(next_page_url, self.parse)

    def parse_details(self,response):
        sales_agents = response.css('div.object-primary > section.object-contact > div > h3.object-contact-aanbieder-name > a::text').extract()
        garden = str(response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(19) > dd:nth-child(4)::text').extract_first()).strip().rstrip("\n").rstrip("\r")
        img_urls = response.css('div.object-media-foto > a > img::attr(src)').extract() + response.css('div.object-media-foto > div > img::attr(data-lazy)').extract()

        yield {
            'zipcode': response.css('#content > div > div > div.object-primary > header > div > div > div.object-header__details-info.fd-m-bottom-l.fd-m-bottom-s--bp-m.fd-flex > div.object-header__container.fd-m-right-xs.fd-flex-grow > h1 > span.object-header__subtitle.fd-color-dark-3::text').extract_first().strip().rstrip("\n").rstrip("\r").replace(" ","")[:6], #Emmanuel
            'sellingPrice': int(re.findall('\d*\,?\d+',response.css('#content > div > div > div.object-primary > header > div > div > div.object-header__pricing.fd-text-size-l.fd-flex--bp-m.fd-align-items-center > div > strong::text').extract_first().strip().rstrip("\n").rstrip("\r"))[0].replace(",","")), #Emmanuel
            'Asking_Price_M2': str(response.xpath("//html/body/main/div/div/div[1]/section[4]/div/dl[1]/dd[2]/text()").extract_first()).strip(), # Emmanuel
            'Services': str(response.xpath("/html/body/main/div/div/div[1]/section[4]/div/dl[4]/dd[5]/text()").extract_first()).strip(), # Emmanuel
            'sales_agent': sales_agents[0] if len(sales_agents)>=1 else None, #Emmanuel
            
            'fulldescription': ''.join(response.css('div.object-description-body *::text').extract()).strip().rstrip("\n").rstrip("\r").replace("  "," ").replace("   "," "), #Baris
            'housetype' : response.xpath('//*[@id="content"]/div/div/div[1]/section[5]/div/dl[2]/dd[1]/text()').get(), # Baris

            'parcelsurface': str(response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd:nth-child(5)::text').extract_first()).strip().rstrip("\n").rstrip("\r"), #Felicia
            'yearofbuilding': str(response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(5) > dd:nth-child(6)::text').extract_first()).strip().rstrip("\n").rstrip("\r"), # Felicia
            'description_garden': str(response.css('div.object-primary > section:nth-child(7) > div > dl:nth-child(19) > dd:nth-child(4)::text').extract_first()).strip().rstrip("\n").rstrip("\r"), # Felicia

            'numberrooms': int(max(re.findall("\d+", response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(11) > dd:nth-child(2)::text').extract_first()))),
            'numberbathrooms': int(max(re.findall("\d+",response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(11) > dd:nth-child(4)::text').extract_first()))),
            'energylabelclass': str(response.css('span.energielabel::text').extract_first()).strip().rstrip("\n").rstrip("\r"),
            'surface': int(max(re.findall("\d+",response.css('#content > div > div > div.object-primary > section:nth-child(7) > div > dl:nth-child(8) > dd:nth-child(5)::text').extract_first()))),
            'buying_agent': sales_agents[1] if len(sales_agents)==2 else None, #Robin
            
            'sellingDate': datetime.strptime(str(response.css('#content > div > div > div.object-primary > section:nth-child(3) > div > dl > dd:nth-child(4)::text').extract_first()).strip().rstrip("\n").rstrip("\r"), '%B %d, %Y').date(),
            'publicationDate': datetime.strptime(str(response.css('#content > div > div > div.object-primary > section:nth-child(3) > div > dl > dd:nth-child(2)::text').extract_first()).strip().rstrip("\n").rstrip("\r"), '%B %d, %Y').date(),
       
            'url': response,
            'image_urls': img_urls,
        }

# Scraper to scrap information about the brokers
# Felicia








# Scraper to scrape the reviews of each sales agent
# Baris

