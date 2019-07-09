# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os


class CrawlingPipeline(object):

    def __init__(self, feed_dir):
        self.feed_dir = feed_dir

    @classmethod
    def from_crawler(cls, crawler):
        feed_dir = crawler.settings['DATA_DIR'] / 'feed'
        return cls(feed_dir)

    def open_spider(self, spider):
        if not os.path.exists(self.feed_dir):
            os.makedirs(self.feed_dir)
        self.file = open(self.feed_dir / f'{spider.name + ".jl"}',
                         mode='a', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        self.file.write(json.dumps(item) + '\n')
        return item

