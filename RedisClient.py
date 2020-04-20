import redis
from random import choice

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxy'

class RedisClient(object):

    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        # 初始化Redis
        self.db = redis.StrictRedis(host,port,password=password,decode_responses=True)

    def add(self,proxy,score=INITIAL_SCORE):
        # 若redis中没有该proxy则增加
        if not self.db.zscore(REDIS_KEY,proxy):
            self.db.zadd(REDIS_KEY,{proxy:score})

    def random(self):
        # 随机获取有效代理，优先选择分数最高的，若分数最高不存在则按分数从高到低选择
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrangebyscore(REDIS_KEY,100,0)
            if len(result):
                return choice(result)
            else:
                print('redis中暂无proxy')

    def decrease(self,proxy):
        # 分数减一，若小于最小值删除
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score>MIN_SCORE:
            print(f'代理{proxy},当前分数{score},减一')
            return self.db.zincrby(REDIS_KEY,-1,proxy)
        else:
            print(f'代理{proxy},当前分数{score},移除')
            return self.db.zrem(REDIS_KEY,proxy)

    def exists(self,proxy):
        # 判断代理是否存在
        result = self.db.zscore(REDIS_KEY,proxy)
        if len(result):
            return True
        else:
            return False

    def max(self,proxy):
        # 将代理设置为最大值
        print(f'代理{proxy}可用,设置为最大值')
        self.db.zadd(REDIS_KEY,{proxy:MAX_SCORE})

    def count(self):
        # 返回redis中代理的数量
        return self.db.zcard(REDIS_KEY)

    def all(self):
        # 返回redis中所有代理
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)
