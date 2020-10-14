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
        path="D:\\Anaconda3\\chromedriver.exe"
        options.add_argument("user-data-dir=D:\data\scrapy" )
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        # options.add_argument("--headless" )
        self.browser = webdriver.Chrome(options=options, executable_path=path)
    def proxy():
        #https://www.hailiangip.com/tool/page/code 代理商使用的地址
        orderId = "O20101117292659712964"
        secret = "58faf5fb12c9424a81d3d5c8fd3574dd"
        host = "flow.ipproxy.info"
        port = "14223"
        user = "proxy"
        timestamp = str(int(time.time()))  # 计算时间戳
        txt = "orderId=" + orderId + "&" + "secret=" + secret + "&" + "time=" + timestamp
        txt = txt.encode()
        sign = hashlib.md5(txt).hexdigest()  # 计算sign
        password = 'orderId=' + orderId + '&time=' + timestamp + '&sign=' + sign + "&pid=-1" + "&cid=-1" + "&uid=" + "&sip=0" + "&nd=0"
        # print(password)
        proxyUrl = "--proxy-server=http://" + user + ":" + password + "@" + host + ":" + port
        # print(proxyUrl)
        return proxyUrl
# proxy_url=proxy()
# options.add_argument(proxy_url)
# options.add_argument("--proxy-server=http://123.156.181.176:4281")

    def make_file(self,filename):
        if os.path.exists(filename):
            pass
            # with open('filename', mode='r', encoding='utf-8') as ff:
                # print(ff.readlines())
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
                    sql = "INSERT INTO keyword(keyword,info,url,title) VALUES(%s,%s,%s,%s)"
                    self.cursor.execute(sql, (keyword, info, url, title))
                    self.cursor.connection.commit()
                    self.mysqlNum = self.mysqlNum + 1
                    print('成功插入数据库的数量:{}'.format(self.mysqlNum))
                except BaseException as e:
                    print("错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")
            except:
                print('出现错误')
    def get_infos_url(self,url,keyword):
        self.browser.get(url)
        lists_infos = self.browser.find_elements_by_class_name('js-fanyi-result')
        if lists_infos:
            self.pare_lists_infos(lists_infos,keyword)
        ##需要验证码的时候
        else:
            while self.flag:
                code=input('请输入验证码:')
                try:
                    self.browser.find_element_by_id('seccodeInput').send_keys(code)
                    self.browser.find_element_by_id('submit').click()
                    time.sleep(5)
                    lists_infos = self.browser.find_elements_by_class_name('js-fanyi-result')
                    if lists_infos:
                        self.pare_lists_infos(lists_infos,keyword)
                        break
                    else:
                        pass
                except Exception as e:
                    print(e)
    def make_url_from_keyword():
        pass
if __name__=="__main__":
    # proxy()

    filename='./test_url.txt'
    page = 4
    url = "https://english.sogou.com/english?query={}&fr=common_nav&b_o_e=1&page={}&ie=utf8&pagenumtype=global"
    with open(r"./test.txt", 'r', encoding='utf-8') as infiles:
        lines=infiles.readlines()
        num=len(lines)
        spider = spider(num)
        print(spider.lines)
        for line in lines:
            spider.currentLine=spider.currentLine+1
            str = line.rstrip('\n')
            keyword=str.replace(' ','+')
            # print('当前关键词:{}'.format(keyword))
            print('总关键词:{},当前第{}个关键词:{}'.format(num,spider.currentLine,str))

            for i in range(1,page):
                page_url=url.format(keyword,i)
                print('第{}页获取到的内容,当前链接地址：{}'.format(i, page_url))
                # write_txt(page_url, filename)
                spider.get_infos_url(page_url,str)
            progress = (spider.currentLine) / spider.lines
            timeLong = time.time() - spider.start_time
            left_time = ((time.time() - spider.start_time) / progress - (timeLong)) / 60
            print('当前进度：{}%,已用时长:{}分钟,预计剩余时间：{}分钟'.format(format(progress * 100, '.2f'), format(timeLong / 60, '.2f'),
                                                          format(left_time, '.2f')))