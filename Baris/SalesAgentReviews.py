import scrapy

class FundaSalesAgentReviewsSpider(scrapy.Spider):
    name = 'FundaSalesAgentReviews'
    allowed_domains =  ['funda.nl']
    start_urls = ['https://www.funda.nl/en/makelaars/heel-nederland/verkoop/soortaanbod-koopwoningen/sorteer-makelaarnaam-op/']

    def parse(self, response):
        print(response.css('div.makelaars-result-item-thumbnail > a::attr(href)').getall())
        for reviewpage in response.css('div.makelaars-result-item-thumbnail > a::attr(href)').getall():
            print('######Reviewpagelink################')
            print(reviewpage)
            yield scrapy.Request(response.urljoin(reviewpage), callback=self.parse_review)

        '''
        # follow pagination link
        next_page_url = response.xpath('//*[@id="content"]/form/div[2]/nav/a/@href').get()
        if len(response.css('#content > form > div.container.search-main.makelaar-search-results-main > nav > a').getall()) == 2:
            next_page_url = response.css('#content > form > div.container.search-main.makelaar-search-results-main > nav > a:nth-child(4)::attr(href)').get()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse)
        '''


    def parse_review(self, response):
        urls = response.css('div > section.makelaars-reviews > div > div > div:nth-child(1) > a::attr(href)').get()
        print('########## LINK TO REVIEW PAGE #################')
        url = response.urljoin(urls)
        yield scrapy.Request(url=url, callback=self.parse_details)


    def parse_details(self, response):
        yield {
            'SalesAgent' : response.css('#content > section > div > div.makelaars-content > h1::text').getall(),
            'Reviews' : ''.join(response.css('div.collapse-text-container::text').getall()).replace("\n","").replace("\r","").replace("  ","").replace("   ","")
            }
        print('################################-FINISHED AGENT-#################################################')

        #MY ADJUSTED CODE IF LEN CODE
        next_page_url = response.css('div.user-reviews.container > div.user-reviews-column-primary > form > nav > a::attr(href)').get()
        if len(response.css('#content > div.user-reviews.container > div.user-reviews-column-primary > form > nav > a').getall()) == 2:
            next_page_url = response.css('#content > div.user-reviews.container > div.user-reviews-column-primary > form > nav > a:nth-child(4)::attr(href)').get()
        next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(url=next_page_url, callback=self.parse_details)