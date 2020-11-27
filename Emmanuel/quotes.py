import scrapy



class QuoteSpide(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://toscrape.com/random']
    
    def parse(self, response):
        self.log('I just visited: '+ response.url)
        yield {
            'author_name': response.css('small.author::text').extract_first(),
            'text': response.css('spann.text::text').extract_first(),
            'tags': response.css('a.tag::text').extract(),
        }
        
'''
        # follow pagination link
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

        
for quote in response.css('div.quote'):
    item = {
        'author_name': quote.css('small.author::text')
        'text': quote.css('spann.text::text').extract_first(),
        'tags': quote.css('a.tag::text').extract_first(),
            
        }
        
'''