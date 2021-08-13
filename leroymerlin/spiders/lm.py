import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LmSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa-product-name]")
        for link in links:
            yield response.follow(link, callback=self.parse_good)
        next = response.xpath('//a[@data-qa-pagination-item="right"]/@href').extract_first()
        if next:
            yield response.follow('https://leroymerlin.ru' + next, callback=self.parse)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price1', "//uc-pdp-price-view[@class='primary-price']/span[@slot='price']/text()")
        loader.add_xpath('price2', "//uc-pdp-price-view[@class='primary-price']/span[@slot='fract']/text()")
        loader.add_xpath('unit1', "//uc-pdp-price-view[@class='primary-price']/span[@slot='unit']/text()")
        loader.add_xpath('price21', "//uc-pdp-price-view[@class='second-price']/span[@slot='price']/text()")
        loader.add_xpath('price22', "//uc-pdp-price-view[@class='second-price']/span[@slot='fract']/text()")
        loader.add_xpath('unit2', "//uc-pdp-price-view[@class='second-price']/span[@slot='unit']/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('term', '//dl[@class ="def-list"]//dt/text()')
        loader.add_xpath('definition', '//dl[@class ="def-list"]//dd/text()')
        loader.add_xpath('photos', "//uc-pdp-media-carousel//img[@itemprop='image']/@src")
        yield loader.load_item()




        # name = response.xpath("//h1/text()").extract_first()
        # price = response.xpath("//span[@class='ProductHeader__price-default_current-price ']/text()").extract_first()
        # photos = response.xpath("//img[@class=' PreviewListSmall__image Image']/@src").extract()
        #
        # yield CitilinkItem(name=name, price=price, photos=photos)

