import selenium
import time
import hashlib
from selenium import webdriver
import os
import threading
import pymysql
from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
from redis_scrapy import RedisQueue
import math
# 采集线程列表
crawl_thread_list = []
for i in range(10):
    crawl_thread_list.append(i)
class BingSpider(threading.Thread):
    def __init__(self,name,num,redisqueue):
        super().__init__()
        self.connect = False
        self.connect = pymysql.connect(
            host="127.0.0.1",
            db="scrapy",
            user="root",
            passwd="root",
            charset='utf8',
            use_unicode=True
        )
        #验证码不正确时一直输入验证码
        self.flag=True
        self.start_time = time.time()
        self.num=num
        self.name=name
        self.currentLine=0
        self.redis_object = redisqueue
        self.mysqlNum=0  #插入数据库的数量
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        options = webdriver.ChromeOptions()
        # path="D:\\Anaconda3\\chromedriver.exe"
        path=r"D:\soft\python\chromedriver.exe"
        options.add_argument("user-data-dir=D:\data\scrapy" )
        # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        options.binary_location = r"C:\Users\CYG\AppData\Local\Google\Chrome\Application\chrome.exe"
        options.add_argument("--headless" )
        self.browser = webdriver.Chrome(options=options, executable_path=path)
    #线程开始的地方
    def run(self):
        while True:
            qsize = self.redis_object.qsize()
            # print('当前线程:{},总数量:{},剩余数量:{}'.format(self.name,self.num,qsize))
            progress = (self.num - qsize + 1) / self.num
            timeLong = time.time() - self.start_time
            left_time = ((time.time() - self.start_time) / progress - (timeLong)) / 60
            per_num = math.ceil((self.num - qsize + 1) / (timeLong / 60))
            print('当前线程:{},总数量:{},剩余数量:{},当前进度：{}%,已用时长:{}分钟,预计剩余时间：{}分钟,平均一分钟:{}个'.format(self.name,self.num,qsize,format(progress * 100,'.2f'),
                                                                    format(timeLong / 60,'.2f'),
                                                                    format(left_time,'.2f'),per_num))
            keyword = self.get_url_info_from_queue()
            if qsize:
                keyword_url = '+'.join(keyword.split(' '))
                url = 'https://cn.bing.com/search?q=' + keyword_url + '&qs=AS&ensearch=1&FORM=BESBTB'
                self.get_infos_url(url,keyword)
            else:
                break
    #解析从搜狐引擎中获取到的列表元素并将（标题，内容，关键词，=》存入数据中）
    def insert_title_info(self,keyword,title,info):
        try:
            sql = "INSERT INTO bing_scrapy(keyword,info,title) VALUES(%s,%s,%s)"
            self.cursor.execute(sql, (keyword, info, title))
            self.cursor.connection.commit()
            self.mysqlNum = self.mysqlNum + 1
            # print('当前线程:{},成功插入数据库的数量:{}'.format(self.name,self.mysqlNum))
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")
            print('重新连接数据库')
            self.connect = pymysql.connect(
                host="127.0.0.1",
                db="scrapy",
                user="root",
                passwd="root",
                charset='utf8',
                use_unicode=True
            )
            self.cursor = self.connect.cursor()
    '''
    根据url地址获取相应的内容 并写入数据库中
    '''
    def get_infos_url(self,url,keyword,page=1):
        self.browser.get(url)
        b_results = self.browser.find_element_by_id('b_results')
        # print(b_results)
        try:
            # algo=b_results.find_elements_by_class_name('b_algo')
            algo=b_results.find_elements_by_xpath("//li[@class='b_algo']")
            for i in algo:
                try:
                    title=i.find_elements_by_tag_name('h2')[0].text
                    info=i.find_elements_by_class_name('b_caption')[0].find_elements_by_tag_name('p')[0].text
                    # print("当前关键词:{},url链接地址:{},标题:{},内容:{}".format(keyword,url,title,info))
                    # print("当前关键词:{},页码:{},标题:{},内容:{}".format(keyword,math.ceil(page/10),title,info))
                    self.insert_title_info(keyword,title,info)
                except Exception as e:
                    print("错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")
            next_page=self.browser.find_elements_by_xpath("//a[@title='Next page']")
            if next_page and page<60:
                page=page+10
                url=url+'&first='+str(page)
                # print('有下一ye')
                self.get_infos_url(url,keyword,page)
            else:
                # print('没有下一页')
                pass
        except Exception as e:
            print("错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")
     # 从队列中获取一个待下载的URL
    def get_url_info_from_queue(self):
        while True:
            url_info = self.redis_object.get_wait(20)
            if url_info is not None and len(url_info) >= 2:
                url_info = url_info[1]
                if url_info is not None:
                    return url_info
            return url_info
def main():
    # 创建页码队列
    redisqueue = RedisQueue('keyword')
    qsize = redisqueue.qsize()
    for i in crawl_thread_list:
        download_thread = BingSpider(i,qsize,redisqueue)
        download_thread.start()
    print(qsize)
    time.sleep(20)
    print('主采集结束')
    pass

if __name__=="__main__":
    # url = "https://cn.bing.com/search?q=jaw+chew+toy&qs=AS&pq=jaw+ch&ensearch=1&FORM=BESBTB"
    # spider=spider(10)
    # spider.get_infos_url(url,'jaw')
    # redisqueue = RedisQueue('keyword')
    # qsize = redisqueue.qsize()
    # spider=spider(qsize,redisqueue)
    # while True and qsize:
    #     qsize = redisqueue.qsize()
    #     print('总数量:{},剩余数量:{}'.format(spider.num,qsize))
    #     progress = (spider.num-qsize+1) / spider.num
    #     timeLong = time.time() - spider.start_time
    #     left_time = ((time.time() - spider.start_time) / progress - (timeLong)) / 60
    #     per_num=math.ceil((spider.num-qsize+1)/(timeLong/60))
    #     print('当前进度：{}%,已用时长:{}分钟,预计剩余时间：{}分钟,平均一分钟:{}个'.format(format(progress * 100, '.2f'), format(timeLong / 60, '.2f'),
    #                                                       format(left_time, '.2f'),per_num))
    #     keyword=spider.get_url_info_from_queue()
    #     if qsize:
    #         keyword_url='+'.join(keyword.split(' '))
    #         url='https://cn.bing.com/search?q='+keyword_url+'&qs=AS&ensearch=1&FORM=BESBTB'
    #         spider.get_infos_url(url,keyword)
    #     else:
    #         break
    main()
    print('爬取结束')