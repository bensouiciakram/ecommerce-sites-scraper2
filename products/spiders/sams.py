import scrapy
from nested_lookup import nested_lookup
from scrapy.loader import ItemLoader 
from products.items import SamsItem


class SamsSpider(scrapy.Spider):
    name = 'sams'
    allowed_domains = ['sams.com.mx']
    start_urls = ['https://www.sams.com.mx/sams/department/electronica-y-computacion/_/N-84u?storeId=0000004910']

    def __init__(self):
        self.image_template_url = 'https://assets.sams.com.mx/image/upload/f_auto,q_auto:eco,w_200,c_scale,dpr_auto/mx/images/product-images/img_small/{}s.jpg'

    def parse(self, response):
        data = response.json()
        products = [product for product in nested_lookup('records',data) if product]
        for product in products : 
            loader = ItemLoader(SamsItem(),response)
            loader.add_value('product_url',product[0]['attributes']['product.seoURL'][0])
            loader.add_value('sku',product[0]['attributes']['sku.repositoryId'][0]) 
            loader.add_value('image_url',self.image_template_url.format(loader._values['sku'][0]))
            loader.add_value('high_price',product[0]['attributes']['sku.lastPrice'][0])
            loader.add_value('low_price',product[0]['attributes']['sku.lastPrice'][0])
            loader.add_value('title',product[0]['attributes']['skuDisplayName'][0])
            #loader.add_value('tags')
            yield loader.load_item()