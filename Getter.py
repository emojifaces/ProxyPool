from CrawlerProxy import Crawler
from RedisClient import RedisClient


POOL_UPPER_THRESHOLD = 1000

class Getter(object):
    def __init__(self):
        self.client = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        if self.client.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('获取器开始执行')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxys = self.crawler.get_proxy(callback)
                for proxy in proxys:
                    self.client.add(proxy)