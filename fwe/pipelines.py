# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os


class FwePipeline(object):

    def open_spider(self, spider):
        if not os.path.exists('./data/feed'):
            os.makedirs('./data/feed')
        self.file = open('./data/feed/%s.jl' % spider.name, 'a', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        self.file.write(json.dumps(item) + '\n')
        return item

