import redis
'''
    redis列表对象操纵
'''
class RedisQueue(object):
    def __init__(self, name):
        # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
        self.__db = redis.Redis(host='127.0.0.1', port=6379,decode_responses=True)  # 链接数据库
        self.key = '%s' % ( name)

    def qsize(self):
        return self.__db.llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, item):
        self.__db.rpush(self.key, item)  # 添加新元素到队列最右方

    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.__db.blpop(self.key, timeout=timeout)
        # if item:
        #     item = item[1]  # 返回值为一个tuple
        return item

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__db.lpop(self.key)
        return item
    def show_queue(self,start=0,end=-1):
        # 默认返回当前对象列表的值
        item = self.__db.lrange("keyword" , start , end)
        return item
'''
    redis集合对象操纵
'''
class RedisSet(object):
    def __init__(self, name):
        # redis的默认参数为：host='localhost', port=6379, db=0， 其中db为定义redis database的数量
        self.__db = redis.Redis(host='127.0.0.1', port=6379)  # 链接数据库
        self.key = '%s' % ( name)

    def size(self):
        return self.__db.scard(self.key)  # 返回集合里面元素的数量

    def put(self, item):
        self.__db.sadd(self.key, item)  # 添加新元素到结合中

    def get(self):
        # 随机返回集合一个元素
        item = self.__db.spop(self.key)
        return item
    def show_all(self,count=1):
        # 默认返回当前对象列表的值
        item = self.__db.smembers(self.key)
        return item
    def show_num(self,count=1):
        # 默认返回当前对象列表的值
        item = self.__db.srandmember(self.key ,count)
        return item
'''
    读取指定的文件 并且把文件中内容放在redis队列中
    流程：text-->line-->redis(list)
'''
def read_text_redis(redis_object,filename=''):
    with open(filename, 'r', encoding='utf-8') as infiles:
        lines = infiles.readlines()
        for line in lines:
           redis_object.put(line.strip('\n'))
if __name__=='__main__':
    filename=r"./sitemap_url.txt"
#     # redis_object=RedisSet('keyword_set')
    redis_object=RedisQueue('keyword_url')
    print(redis_object.qsize())
    # read_text_redis(redis_object,filename)
