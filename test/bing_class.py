import selenium
import time
import hashlib
from selenium import webdriver
import os
import pymysql
from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
class spider:
    def __init__(self,num):
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
        self.lines=num
        self.currentLine=0
        self.mysqlNum=0  #插入数据库的数量
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        options = webdriver.ChromeOptions()
        # path="D:\\Anaconda3\\chromedriver.exe"
        path=r"D:\soft\python\chromedriver.exe"
        options.add_argument("user-data-dir=D:\data\scrapy" )
        # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        options.binary_location = r"C:\Users\CYG\AppData\Local\Google\Chrome\Application\chrome.exe"
        # options.add_argument("--headless" )
        self.browser = webdriver.Chrome(options=options, executable_path=path)

    def make_file(self,filename):
        if os.path.exists(filename):
            pass
        else:
            with open(filename, mode='w', encoding='utf-8') as ff:
                print("文件创建成功！")
    def write_txt(self,keyword,filename):
        self.make_file(filename)
        with open(filename, "a", encoding='utf-8') as f:
            f.write(keyword+'\n')
    ##删除中断时txt文本中已经用过的关键词
    def del_txt(self):
        pass
    #解析从搜狐引擎中获取到的列表元素并将（标题，内容，关键词，=》存入数据中）
    def pare_lists_infos(self,lists_infos,keyword):
        for list in lists_infos:
            # print(list)
            try:
                title = list.find_element_by_tag_name('h3').text
                try:
                    info = list.find_element_by_class_name('ft').text
                except:
                    info = list.find_element_by_class_name('str_info').text
                print('关键词:' + keyword + '     标题内容为:' + title)
                print('详情内容：' + info)
                try:
                    sql = "INSERT INTO bing_scrapy(keyword,info,url,title) VALUES(%s,%s,%s,%s)"
                    self.cursor.execute(sql, (keyword, info, url, title))
                    self.cursor.connection.commit()
                    self.mysqlNum = self.mysqlNum + 1
                    print('成功插入数据库的数量:{}'.format(self.mysqlNum))
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
            except:
                print('出现错误')
    def get_infos_url(self,url,keyword):
        self.browser.get(url)
        b_results = self.browser.find_element_by_id('b_results')
        print(b_results)
        algo=b_results.find_elements_by_class_name('b_algo')
        print(algo)
        for i in algo:
            print(i)
            print(i.find_elements_by_tag_name('h2')[0].text)

    def get_url_info_from_queue(self):
       pass
if __name__=="__main__":
    # proxy()

    filename='./test_url.txt'
    page = 4
    url = "https://cn.bing.com/search?q=jaw+chew+toy&qs=AS&pq=jaw+ch"
    spider=spider(10)
    spider.get_infos_url(url,'jaw')