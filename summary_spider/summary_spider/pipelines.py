# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo


class SummarySpiderPipeline:

    def __init__(self):
        self.asia_uri = 'mongodb://asia.mongo.pub.spider:nVPVEfWNsekzD7XOKnAPq3hlDty2sRkt@pub.mongo.asia.nb.com:27017/?replicaSet=pub&readPreference=secondaryPreferred&authSource=admin'
        self.na_uri = 'mongodb://i18n.mongo.pub.api:Dpv3VQHDnwSPktwkHA1pM3qTFD9CvgTR@pub.mongo.i18n.nb.com:27017/?replicaSet=pub&readPreference=secondaryPreferred&authSource=admin'
        self.sa_uri = 'mongodb://sa.mongos.pub.spider:vUfYVimomzJ97gzHeXQ4xNKb7WJoQ2Uz@pub.mongos.sa.nb.com:27017/?authSource=admin'
        self.euro_uri = 'mongodb://euro.mongo.pub.spider:JPFKZH7oCjf3ZnJWZTSANcM2x3dkP6Ck@pub.mongo.euro.nb.com:27017/?replicaSet=pub&readPreference=secondaryPreferred&authSource=admin'
        self.db = pymongo.MongoClient(self.asia_uri)['spider_i18n']
        self.col_dic = {'60second': self.db['60second_summary'],
                        'bshort': self.db['bshortnews_summary'],
                        'npr': self.db['npr_summary']}

    def process_item(self, item, spider):
        dic = {'title': item['title'],
               'summary': item['summary'],
               'ts': item['ts'],
               'origin_url': item['origin_url'],
               'summary_url': item['summary_url'],
               'pubilish_time': item['publish_time']

               }
        col = self.col_dic.get(item.get('website'))
        print(dic)
        # col.insert_one(dic)


