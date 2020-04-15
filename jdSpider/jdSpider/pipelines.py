# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json


class JdspiderPipeline(object):

    def open_spider(self, spider):
        try:
            self.file = open('phone_info_j2.json', 'w', encoding='utf-8')
            self.file.write('[\n')
        except Exception as err:
            print(err)

    def process_item(self, item, spider):
        dict_item = dict(item)
        json_str = '\t\t' + json.dumps(dict_item, ensure_ascii=False) + ',\n'
        print('==============================================================================')
        print(json_str)
        self.file.write(json_str)
        return item

    def close_spider(self, spider):
        self.file.write('\t]')
        self.file.close()
        print("================================================================")