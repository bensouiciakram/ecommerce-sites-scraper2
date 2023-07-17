# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst




# a function that help to delete $ and , from the price 
def delete_ponctuation_from_price(price_list):
    if type(price_list[0]) in [int,float]:
        return price_list
    return [float(price.replace('$','').replace(',','')) for price in price_list]

# a function that help to delete " and , from the title 
def delete_ponctuation_from_title(title_list):
    return [title.replace('"','').replace(',','') for title in title_list]


class WalmartItem(scrapy.Item):
    product_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        input_processor = delete_ponctuation_from_title,
        output_processor=TakeFirst()
    )
    brand = scrapy.Field()
    high_price = scrapy.Field(
        input_processor = delete_ponctuation_from_price,
        output_processor=TakeFirst()
    )
    low_price = scrapy.Field(
        input_processor = delete_ponctuation_from_price,
        output_processor=TakeFirst()
    )
    discount_price = scrapy.Field(
        output_processor=TakeFirst()
    )
    sku = scrapy.Field(
        output_processor=TakeFirst()
    )
    subcategory = scrapy.Field(
        output_processor = TakeFirst()
    )
    date = scrapy.Field(
        output_processor = TakeFirst()  
    )

class ElektraItem(scrapy.Item):
    product_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        input_processor = delete_ponctuation_from_title,
        output_processor=TakeFirst()
    )
    brand = scrapy.Field()
    high_price = scrapy.Field(
        input_processor = delete_ponctuation_from_price,
        output_processor=TakeFirst()
    )
    low_price = scrapy.Field(
        input_processor = delete_ponctuation_from_price,
        output_processor=TakeFirst()
    )
    discount = scrapy.Field(
        output_processor=TakeFirst()
    )
    sku = scrapy.Field(
        output_processor=TakeFirst()
    )

class SamsItem(scrapy.Item):
    product_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    title = scrapy.Field(
        input_processor = delete_ponctuation_from_title,
        output_processor=TakeFirst()
    )
    high_price = scrapy.Field(
        input_processor = delete_ponctuation_from_price,
        output_processor=TakeFirst()
    )
    low_price = scrapy.Field(
        input_processor = delete_ponctuation_from_price,
        output_processor=TakeFirst()
    )
    tags = scrapy.Field(
        output_processor=TakeFirst()
    )
    sku = scrapy.Field(
        output_processor=TakeFirst()
    )

    