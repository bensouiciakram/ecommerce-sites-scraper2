import scrapy
from scrapy.loader import ItemLoader
from products.items import ElektraItem
import json 
from re import search 
from scrapy import Request

class ElektraSpider(scrapy.Spider):
    name = 'elektra'
    allowed_domains = ['elektra.com.mx']
    start_urls = [
        'https://www.elektra.com.mx/electronica/tv-y-video',
        'https://www.elektra.com.mx/electronica/accesorios-para-electronica',
         'https://www.elektra.com.mx/electronica/instrumentos-musicales',
        'https://www.elektra.com.mx/electronica/audio-y-equipos-de-sonido',
        'https://www.elektra.com.mx/electronica/equipos-de-radiofrecuencia',
        'https://www.elektra.com.mx/electronica/accesorios-para-camaras',
        'https://www.elektra.com.mx/electronica/camaras',
        'https://www.elektra.com.mx/electronica/audio-para-autosx'
        ]

    def __init__(self):
        self.product_template_url = 'https://www.elektra.com.mx/{}/p'
        self.products_template_url = 'https://www.elektra.com.mx/electronica/tv-y-video?map=category-1&page={}&query=/electronica&searchState'

    def start_requests(self):
        for url in self.start_urls :
            yield Request(
                url,
                meta={
                    'page':1,
                    'base_url':url
                }
            )
    def parse(self, response):
        
        data = json.loads(response.xpath('//template[@data-varname="__STATE__"]/script/text()').get())
        products_urls = [key for key in data.keys() if bool(search('Product[\s\S]+\d{3,}$',key))]
        if not products_urls :
            return
        images = [data[img]['imageUrl'] for img in self.get_products_images(data)]

        for product,image in zip(products_urls,images) :
            loader = ItemLoader(ElektraItem(),response)
            loader.add_value('product_url',self.get_product_url(data,product))
            loader.add_value('image_url',image)
            loader.add_value('title',data[product]['productName'])
            loader.add_value('brand',data[product]['brand'])
            loader.add_value('high_price',self.get_high_price(data,product))
            loader.add_value('low_price',self.get_low_price(data,product))
            try:
                loader.add_value('discount','{:.2f}'.format(((loader._values['high_price'][0]-loader._values['low_price'][0])/loader._values['high_price'][0])*100))
            except :
                pass
            loader.add_value('sku',data[product]['productId'])
            yield loader.load_item()
        
        page = response.meta['page']
        base_url = response.meta['base_url']
        yield Request(
            base_url + '?page={}'.format(page+1),
            meta ={
                'page':page + 1,
                'base_url':base_url
            }
        )

    def get_product_url(self,data,product):
        return self.product_template_url.format(
            data[product]['linkText']
        )

    def get_products_images(self,data):
        imgs_keys = [key for key in data.keys() if 'Image' in key]
        imgs = set()
        add = True
        for key in data.keys():
            if 'Image' in key:
                if add :
                    imgs.add(key)
                    add = False
                else:
                    add =True
        return imgs

    def get_low_price(self,data,product_url):
        return data['$' + product_url + '.priceRange.sellingPrice']['highPrice']

    def get_high_price(self,data,product_url):
        return data['$' + product_url + '.priceRange.listPrice']['highPrice']

