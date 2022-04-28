from abc import ABC

import scrapy
from summary_spider.items import SummarySpiderItem
from summary_spider.check_duplicate import latest_60second
import datetime
import re


class SixtySecondSpider(scrapy.Spider):
    name = '60second'
    # allowed_domains = ['example.com']
    start_urls = ['http://example.com/']
    headers = {
        "accept": 'application/json, text/javascript, */*; q=0.01',
    }
    range_num = 1000
    def parse_(self, response):
        item = SummarySpiderItem()
        xpath = '//div[@class="post-container"]'
        check_duplicate = False
        current_num = response.meta['current']
        # print(response.xpath('//div[@class="article-datetime"]').get())
        for news in response.xpath(xpath):
            origin_url_xpath = 'div[2]/div[1]/a/@href'
            item['origin_url'] = news.xpath(origin_url_xpath).get()
            if item['origin_url'] == latest_60second:
                check_duplicate = True
                break
            xpath_summary = 'div[1]/div[2]/div[2]/p/text()'
            item['summary'] = news.xpath(xpath_summary).get()
            item['ts'] = str(
                datetime.datetime.strptime(str(datetime.datetime.utcnow()).split('.')[0], '%Y-%m-%d %H:%M:%S'))
            xpath_time = 'div[1]/div[2]/div[1]'
            time = re.findall('</a>( -.*?)</div>',news.xpath(xpath_time).get())[0]
            item['publish_time'] = self.handle_time(time)
            title_xpath = 'div[1]/div[@class="article-content"]/h2/text()'
            item['title'] = news.xpath(title_xpath).get()
            item['summary_url'] = 'https://www.60secondsnow.com/'
            item['website'] = '60second'
            yield item
        if current_num < self.range_num and not check_duplicate:
            current_num += 1
            yield scrapy.Request(f"https://www.60secondsnow.com/scripts/controller.php?module=homepage&sub_module=homepage-ajax&page_number={current_num}",
                                 callback=self.parse_, meta={'current': current_num})
    def start_requests(self):
        yield scrapy.Request(
            f"https://www.60secondsnow.com/scripts/controller.php?module=homepage&sub_module=homepage-ajax&page_number=1",
            callback=self.parse_,meta={'current': 1})

    @staticmethod
    def handle_time(time):
        date = datetime.datetime.utcnow()
        if 'min' in time:
            if 'hr' in time:
                min_ = int(re.findall('hr, (.*?) min', time)[0])
            else:
                min_ = int(re.findall('- (.*?) min', time)[0])
            date -= datetime.timedelta(minutes=min_)
        if 'hr' in time:
            if 'day' in time:
                hour = int(re.findall('days?, (.*?) hr', time)[0])
            else:
                hour = int(re.findall('- (.*?) hr', time)[0])
            date -= datetime.timedelta(hours=hour)
        if 'day' in time:
            day = int(re.findall('- (.*?) day', time)[0])
            date -= datetime.timedelta(days=day)

        return str(date)
