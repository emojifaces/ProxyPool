import asyncio
import time

from RedisClient import RedisClient
import aiohttp

VALTD_STATUS_CODES = [200]
TEST_URL = 'www.baidu.com'
BATCH_TEST_SIZE = 10


class Tester(object):
    def __init__(self):
        self.client = RedisClient()

    async def test_single_proxy(self,proxy):

        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://'+proxy
                print('正在测试',proxy)
                async with session.get(TEST_URL,proxy=real_proxy,timeout=15) as response:
                    if response.status == VALTD_STATUS_CODES:
                        self.client.max(proxy)
                        print('代理可用',proxy)
                    else:
                        self.client.decrease(proxy)
                        print('代码不可用',proxy)
            except (TimeoutError):
                self.client.decrease(proxy)
                print('代理请求失败',proxy)

    def run(self):
        print('测试器开始运行')
        try:
            proxys = self.client.all()
            loop = asyncio.get_event_loop()
            for i in range(0,len(proxys),BATCH_TEST_SIZE):
                test_proxys = proxys[i:i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxys]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误',e.args)