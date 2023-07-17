# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ProductsPipeline:
    def __init__(self):
        self.skus = set()


    def process_item(self, item, spider):
        if not item['sku'] in self.skus :
            self.skus.add(item['sku'])
            return item
        else :
            raise DropItem('duplicate item')
