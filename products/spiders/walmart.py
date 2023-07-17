import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from products.items import WalmartItem
from scrapy.shell import inspect_response
from datetime import datetime 

class WalmartSpider(scrapy.Spider):
    name = 'walmart'
    allowed_domains = ['walmart.com.mx']
    start_urls = ['https://www.walmart.com.mx/api/v2/page/department/computadoras']

    def __init__(self):
        self.family_base_url = 'https://www.walmart.com.mx/api/v2/page/family'
        self.category_base_url = 'https://www.walmart.com.mx/api/v2/page/browse'
        self.product_url_template = 'https://www.walmart.com.mx/api/rest/model/atg/commerce/catalog/ProductCatalogActor/getProduct?id={}'

    # extract all the families urls and send request to them 
    def parse(self, response):
        data = response.json()
        families_urls = [family['url'] for family in data['navigation']['refinements']]
        for family_url in families_urls :
            yield Request(
                self.family_base_url + family_url,
                callback = self.parse_category
            )

    # extract all the categories urls  of a family
    def parse_category(self,response):
        data = response.json()
        categories_urls = [category['url'] for category in data['navigation']['refinements']]
        for category_url in categories_urls :
            yield Request(
                self.category_base_url + category_url +'?size=50&page=0',
                callback=self.parse_products_urls,
                meta ={
                    'category_url':category_url
                }
            )

    # extract all the product urls 
    def parse_products_urls(self,response):
        data = response.json()

        products_ids = [product['productId'] for product in data['appendix']['SearchResults']['content']]
        for product_id in products_ids :
            yield Request(
                self.product_url_template.format(product_id),
                callback = self.parse_product
            )

        total_pages = data['appendix']['SearchResults']['totalPages']
        current_page = int(response.url.split('=')[-1])
        if current_page < total_pages : 
            yield Request(
                self.category_base_url + response.meta.get('category_url') + f'?size=50&page={current_page + 1}',
                callback = self.parse_products_urls,
                meta ={
                    'category_url':response.meta.get('category_url')
                }
            )

    def parse_product(self,response):
        data = response.json()['product']
        loader = ItemLoader(WalmartItem(),response)
        loader.add_value('product_url','https://www.walmart.com.mx' + data['productSeoUrl'])
        loader.add_value('image_url','https://www.walmart.com.mx' + data['childSKUs'][0]['largeImageUrl'])
        loader.add_value('title',data['displayName'])
        loader.add_value('brand',data['brand'])
        loader.add_value('high_price',data['childSKUs'][0]['offerList'][0]['priceInfo']['originalPrice'])
        loader.add_value('low_price',data['childSKUs'][0]['offerList'][0]['priceInfo']['specialPrice'])
        loader.add_value('discount_price',loader._values['high_price'][0]-loader._values['low_price'][0])
        loader.add_value('sku',data['repositoryId'])
        loader.add_value('subcategory',data['breadcrumb']['familyName'])
        loader.add_value('date',str(datetime.now()))
        yield loader.load_item()