import scrapy


class FundaSalesAgentReviewsSpider(scrapy.Spider):
    name = 'FundaSalesAgentReviews'
    allowed_domains =  ['funda.nl']
    start_urls = ['https://www.funda.nl/en/makelaars/heel-nederland/verkoop/soortaanbod-koopwoningen/sorteer-makelaarnaam-op/']
    def parse(self, response):
        for reviewpage in response.css('div.makelaars-result-item-thumbail > a::attr(href)').get():
            yield scrapy.Request(url=url, callback=self.parse_review)
        
        # follow pagination link
        next_page_url = response.xpath('//*[@id="content"]/form/div[2]/nav/a/@href').get()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
    
    def parse_review(self, response):
        urls = response.css('div > section.makelaars-reviews > div > div > div:nth-child(1) > a::attr(href)').get()
        for urls in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)
        # follow pagination link on review page
        next_page_url1 = response.xpath('//*[@id="content"]/div[2]/div[1]/form/nav/a/@href').get()
        if next_page_url1:
            next_page_url1 = response.urljoin(next_page_url1)
            yield scrapy.Request(url=next_page_url1, callback=self.parse_review)
    
    def parse_details(self, response):
        yield {
            'Reviews' : response.css('div.collapse-text-container::text').getall()
            }