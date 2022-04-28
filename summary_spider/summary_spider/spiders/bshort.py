import scrapy
from summary_spider.items import SummarySpiderItem
from scrapy.http import JsonRequest
from summary_spider.check_duplicate import latest_bshort
import datetime
import json


class ExampleSpider(scrapy.Spider):
    name = 'bshort'
    # allowed_domains = ['example.com']
    start_urls = ['http://example.com/']
    headers = {
        "accept": 'application/json, text/javascript, */*; q=0.01',
    }
    range_num = 1000

    def parse_(self, response):
        data = json.loads(response.body.decode())
        item = SummarySpiderItem()
        check_duplicate = False
        current_num = response.meta['current']
        for news in data['news']:
            item['origin_url'] = news['sourceURL']
            if item['origin_url'] == latest_bshort:
                check_duplicate = True
                break
            item['title'] = news['header']
            item['summary'] = news['content']
            item['ts'] = str(datetime.datetime.strptime(str(datetime.datetime.utcnow()).split('.')[0],'%Y-%m-%d %H:%M:%S'))
            item['summary_url'] = 'https://bshortnews.com/'
            item['publish_time'] = news['timeStamp'].split('.')[0]
            item['website'] = 'bshort'
            yield item
        if current_num < self.range_num and not check_duplicate:
            current_num += 1
            data = {"page": current_num}
            yield JsonRequest("https://bshortnews.com/service/api/user/news", data=data,
                              callback=self.parse_, meta={'current': current_num})
    def start_requests(self):
        # for i in range(1009):

        data = {"page": 1}
        yield JsonRequest("https://bshortnews.com/service/api/user/news", data=data,
                          callback=self.parse_,meta={'current': 1})
