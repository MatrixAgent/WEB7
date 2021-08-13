# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import os


class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongobase['goods']
        if item.get('price2') is not None:
            item['price1'] += f".{item['price2']}"
            del item['price2']
        item['price1'] = float(item['price1'].replace(' ', ''))
        if item.get('price21') is not None:
            if item.get('price22') is not None:
                item['price21'] += f".{item['price22']}"
                del item['price22']
            item['price21'] = float(item['price21'].replace(' ', ''))
        item["spec"] = dict(zip(item["term"], item["definition"]))
        del item["term"]
        del item["definition"]
        collection.update_one({'url': item['url']}, {'$set': dict(item)}, upsert=True)
        return item

class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'full/{item["name"]}/{os.path.basename(request.url)}'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
