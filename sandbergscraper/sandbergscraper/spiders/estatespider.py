import scrapy

from sandbergscraper.items import estateItem


class EstatespiderSpider(scrapy.Spider):
    name = "estatespider"
    allowed_domains = ["sandberg-estates.com"]

    # start at page 1
    start_urls = [
        "https://sandberg-estates.com/search-properties?beds=1&baths=1&page=1&pageSize=8&orderBy=RECENTS"
    ]

    def parse(self, response):
        estates = response.css('property-card article.sb-property')
        for estate in estates:
            estate_url = estate.css('a.sb-property__links::attr(href)').get()
            if estate_url:
                estate_url = response.urljoin(estate_url)
                #yield {'url': estate_url}  
                yield response.follow(estate_url, callback=self.parse_estate_page)

        # Check if "Next" button exists
        next_button = response.xpath('//div[contains(@class, "pager-button")]/a[@aria-label="Next page"]')
        if next_button:
            # extract current page from URL
            import re
            m = re.search(r'page=(\d+)', response.url)
            if m:
                current_page = int(m.group(1))
                next_page = current_page + 1
                next_url = re.sub(r'page=\d+', f'page={next_page}', response.url)
                print("#NEW page##################################################\n", next_url)
    
                yield response.follow(url=next_url, callback=self.parse)
        
    def parse_estate_page(self, response):

        estate_Item= estateItem()


        estate_Item['url']=response.url
        estate_Item['title'] =response.css('div.sb-property-page__info div.sb-property-page__tools div div h1::text' ).get()

        estate_Item['price']=response.xpath('//div[contains(@class,"propertyrequest")]/text()').get()

        estate_Item['build_area']=response.xpath('//ul[contains(@class,"sb-property-icons")]/li[span[text()="Build Area"]]/span[2]/text()').get()
        estate_Item['plot_size']=response.xpath('//ul[contains(@class,"sb-property-icons")]/li[span[text()="Plot Size"]]/span[2]/text()').get()
        estate_Item['bath_rooms']=response.xpath('//ul[contains(@class,"sb-property-icons")]/li[span[text()="Bathrooms"]]/span[2]/text()').get()
        estate_Item['bed_rooms']= response.xpath('//ul[contains(@class,"sb-property-icons")]/li[span[text()="Bedrooms"]]/span[2]/text()').get()
        estate_Item['description']=response.xpath(
            '//h2[contains(text(),"About this property")]/following-sibling::div[1]//text()'
        ).getall()
        estate_Item['location_desc']=response.xpath(
            '//h2[contains(text(),"About Area")]/following-sibling::div[1]//text()'
        ).getall()

        yield estate_Item


