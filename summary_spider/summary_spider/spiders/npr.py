import scrapy
from summary_spider.items import SummarySpiderItem
from summary_spider.check_duplicate import latest_npr
import datetime


class ExampleSpider(scrapy.Spider):
    name = 'npr'
    # allowed_domains = ['example.com']
    start_urls = ['http://example.com/']
    headers = {
        "accept": 'application/json, text/javascript, */*; q=0.01',
    }
    range_num = 40

    def parse_(self, response):
        item = SummarySpiderItem()
        xpath = '//div[@class="item-info"]'
        check_duplicate = False
        current_num = response.meta['current']
        for news in response.xpath(xpath):
            try:
                origin_url_xpath = 'h2/a/@href'
                item['origin_url'] = news.xpath(origin_url_xpath).get()
                if item['origin_url'] == latest_npr:
                    check_duplicate = True
                    break
                xpath_summary = 'p[@class="teaser"]/a/text()'
                item['summary'] = news.xpath(xpath_summary).get()
                item['ts'] = str(
                    datetime.datetime.strptime(str(datetime.datetime.utcnow()).split('.')[0], '%Y-%m-%d %H:%M:%S'))
                xpath_time = 'p[@class="teaser"]/a/time/@datetime'
                item['publish_time'] = news.xpath(xpath_time).get()
                title_xpath = 'h2/a/text()'
                item['title'] = news.xpath(title_xpath).get()

                item['summary_url'] = 'https://www.npr.org/sections/news/'
                item['website'] = 'npr'
                yield item
            except:
                pass
        if current_num < self.range_num and not check_duplicate:
            current_num += 1
            yield scrapy.Request(f"https://www.npr.org/get/1001/render/partial/next?start={1 + current_num * 24}",
                                 callback=self.parse_, meta={'current': current_num})

    def start_requests(self):
        yield scrapy.Request(f"https://www.npr.org/get/1001/render/partial/next?start=1",
                             callback=self.parse_, meta={'current': 1})
