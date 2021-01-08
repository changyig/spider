import selenium
import time
import hashlib
from selenium import webdriver
import os
import pymysql
from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
import time
import hashlib
class spider:
    def __init__(self):
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
        self.currentLine=0
        self.mysqlNum=0  #插入数据库的数量
        self.mysqlrelation=0  #插入数据库的数量
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        self.options = webdriver.ChromeOptions()
        # self.path="D:\\Anaconda3\\chromedriver.exe"
        self.path=r"D:\soft\python\chromedriver.exe"
        self.options.add_argument("user-data-dir=D:\data\scrapy" )
        # self.options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.options.binary_location = r"C:\Users\CYG\AppData\Local\Google\Chrome\Application\chrome.exe"
        # options.add_argument("--headless" )
        self.browser = webdriver.Chrome(options=self.options, executable_path=self.path)

    '''
        依据不同的选择器方式，获取页面的中想要获取的指定的元素 
        参数：style:选择器方式 handle:当前对象（浏览器对象或者父对象） pattern:定位元素的类属性之类的 more:返回多个对象或者一个对象 
        返回的数据：1.selenium对象 2.false
        '''

    def try_selector(self,style='css',handle='',pattern='',more=False):
        try:
            if style == 'css':
                if more:
                    content = handle.find_elements_by_css_selector(pattern)
                else:
                    content = handle.find_element_by_css_selector(pattern)
            elif style == 'xpath':
                if more:
                    content = handle.find_elements_by_xpath(pattern)
                else:
                    content = handle.find_element_by_xpath(pattern)
            elif style == 'id':
                if more:
                    content = handle.find_elements_by_id(pattern)
                else:
                    content = handle.find_element_by_id(pattern)
            else:
                if more:
                    content = handle.find_elements_by_tag_name(pattern)
                else:
                    content = handle.find_element_by_tag_name(pattern)
            return content
        except Exception as e:
            print(e)
            return False
    ##问答页内容的数据存入到数据库 : 抓取到的问答页面->解析和过滤数据->存入数据库（数据唯一性判断）
    def answer_insert_mysql(self,data,tablename='zhidao_scrapy'):
        str_md5=(data['url']+str(data['author'])).encode(encoding='UTF-8')
        onlyid= hashlib.md5(str_md5).hexdigest()
        try:
            sql = "INSERT INTO {}(keyword,title,answer,url,onlyid,date) VALUES(%s,%s,%s,%s,%s,%s)".format(tablename)
            self.cursor.execute(sql,(data['title'],data['title'],data['content'],data['url'],onlyid,data['date']))
            self.cursor.connection.commit()
            self.mysqlNum = self.mysqlNum + 1
            print('问答页面成功插入数据库的数量:{},title:{}'.format(self.mysqlNum,data['title']))
        except BaseException as e:
            print("问答页面错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")
        pass

    ##相关性标题的数据存入到数据库 : 抓取到主页面相关问题->解析和过滤数据->存入数据库（数据唯一性判断）
    def relation_insert_mysql(self,data,tablename='zhidao_relation'):
        try:
            sql = "INSERT INTO {}(keyword,url,title,origin,date) VALUES(%s,%s,%s,%s,%s)".format(tablename)
            self.cursor.execute(sql,(data['title'],data['url'],data['title'],data['origin'],data['date']))
            self.cursor.connection.commit()
            self.mysqlrelation = self.mysqlrelation + 1
            print('主页面或者问答页面话题相关性成功插入数据库的数量:{}，title:{}'.format(self.mysqlrelation,data['title']))
        except BaseException as e:
            print("主页面或者问答页面话题相关性成功插入数据库的数量错误在这里>",e,"<错误在这里")

    ##处理获取到的数据:
    def filter_data(self,data):
        pass
    ##处理获取到url链接地址
    def filter_url(self,url):
        res = url.split("'")
        return res[-2]

    #获取问答页面下的相关性问题
    def get_footer_relate(self):
        #相关问题
        data={}
        print('获取问答页面的相关问题')
        relate_list = self.try_selector('css',self.browser,"div.related-list")
        if relate_list:
            item_lists = self.try_selector('css',relate_list,"li.relate-li",True)
            if item_lists:
                for item_list in item_lists:
                    item_span=self.try_selector('css',item_list,"span.related-restrict-title")
                    item_a=self.try_selector('css',item_list,"a")
                    if item_span and item_a:
                        data['url']=item_a.get_attribute("href")
                        data['title']=item_span.text
                        data['origin'] = 2
                        data['date'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                        self.relation_insert_mysql(data)
                    else:
                        pass
                    # print(item_lists)
                    # print(data)
    #获取主页面下的相关性标题和链接
    def get_footer_keyword(self):
        data={}
        footer_container=self.try_selector('css',self.browser,"div.c-container")
        if footer_container:
            span_item=self.try_selector('css',footer_container,"span.rw-item",True)
            if span_item:
                for item in span_item:
                    a=self.try_selector('xpath',item,".//a")
                    if a:
                        url=a.get_attribute("onclick")
                        data['title']=item.text
                        data['url']=self.filter_url(url)
                        data['origin']=1
                        data['date'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                        # print(data)
                        self.relation_insert_mysql(data)
            else:
                print('无内容item')
        else:
            print('无内容container')

    #问答页抓取相关内容 注意流程：打开新的界面->切换成新的窗口句柄->抓取内容->关闭新窗口句柄->返回上一个窗口句柄
    def anwser_infos(self,url=''):
        time.sleep(1)
        cmd = 'window.open("' + url + '")'
        self.browser.execute_script(cmd)
        window = self.browser.window_handles
        self.browser.switch_to.window(window[1])
        article = self.browser.find_element_by_tag_name('article')
        title = self.try_selector('xpath',self.browser,'//h1[@accuse="qTitle"]')
        if title:
            title = title.text
        else:
            title = ''
        if article:
            try:
                #判断是否含有隐藏的内容
                hide_content = self.try_selector('id',self.browser,"show-answer-hide")
                if hide_content:
                    self.browser.execute_script("arguments[0].click();",hide_content)
                hide_content = self.try_selector('css',self.browser,"div.show-answer-dispute")
                if hide_content:
                    self.browser.execute_script("arguments[0].click();",hide_content)
                answers = self.try_selector('css',article,".bd,.answer",True)
                #展开所有隐藏的元素
                for answer in answers:
                    content = self.try_selector('css',answer,"div.answer-text")
                    if content:
                        answer_mask = self.try_selector('css',answer,"div.wgt-answers-showbtn")
                        if answer_mask:
                            print('含有隐藏的数据')
                            self.browser.execute_script("arguments[0].click();",answer_mask)
                    else:
                        answer_mask = self.try_selector('css',answer,"div.wgt-best-showbtn")
                        if answer_mask:
                            print('含有隐藏的数据')
                            self.browser.execute_script("arguments[0].click();",answer_mask)
                time.sleep(1)
                #获取需要的元素
                answers = self.try_selector('css',article,".bd,.answer",True)
                i = 1
                for answer in answers:
                    print("标题:{},第{}个人的回答,当前的链接地址:{}".format(title,i,url))
                    content = self.try_selector('css',answer,"div.answer-text")
                    data_content = ''
                    if content:
                        # print(content.text)
                        data_content = content.text
                    else:
                        print('.line.content div')
                        line = self.try_selector('css',answer,"div[class='line content'] div")
                        if line:
                            # print(line.text)
                            data_content = line.text
                    data = {}
                    data['title'] = title
                    data['author'] = i
                    data['content'] = data_content
                    data['url'] = url
                    data['date'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                    self.answer_insert_mysql(data)
                    # print(data)
                    i = i + 1
                #获取问答页面下的相关问题
                self.get_footer_relate()
                #判断是否含有下一页
                time.sleep(1)
                next_page = self.try_selector('css',self.browser,"a[class='pager-next']")
                if next_page:
                    next_page_url = next_page.get_attribute("href")
                    print('下一页链接地址:{}'.format(next_page_url))
                    self.browser.close()
                    self.browser.switch_to.window(window[0])
                    self.anwser_infos(next_page_url)
                else:
                    print('没有分页关闭第二层分页的窗口')
                    self.browser.close()
                    self.browser.switch_to.window(window[0])
            except Exception as e:
                print(e)
        pass
    #根据关键词抓取主的内容
    def get_infos_url(self,url,url2='',flag=False):
        # self.browser.get(url)
        self.browser.execute_script("window.location.href = '{}';".format(url))
        if flag and url2:
            self.browser.execute_script("window.location.href = '{}';".format(url2))
        # cookies=self.browser.get_cookies()
        # print(cookies)
        # for cookie in cookies:
        #     self.browser.add_cookie(cookie)
        try:
            # infos_container = self.browser.find_element_by_xpath('//div[@class="list-inner"]')
            infos_container = self.try_selector('xpath',self.browser,'//div[@class="list-inner"]')
            if infos_container:
                infos_list=infos_container.find_elements_by_tag_name('dl')
                for infos in infos_list:
                    title=infos.find_element_by_xpath('.//a')
                    a_url=title.get_attribute("href")
                    if a_url:
                        pass
                        self.anwser_infos(a_url)
            #页面底部相关信息的链接 获取->存入数据库->下次调用
            foot_list = self.try_selector('xpath',self.browser,'//div[@class="list-footer"]')
            if foot_list:
                # print(foot_list.text)
                self.get_footer_keyword()
                pass
            #下一页
            page_next = self.try_selector('xpath',self.browser,'//a[@class="pager-next"]')
            if page_next:
                next_page_url=page_next.get_attribute("href")
                print('主页下一个页,链接地址:{}'.format(next_page_url))
                self.get_infos_url(next_page_url)
        except Exception as e:
            print(e)

if __name__=="__main__":
    keyword = '破碎机'
    # url2 = "https://zhidao.baidu.com/search?word=%C6%C6%CB%E9%BB%FA%D3%D0%C4%C4%D0%A9%D6%D6%C0%E0&ie=gbk&site=-1&sites=0&date=0&pn=100"
    # url1 = "https://zhidao.baidu.com/question/1430633872239462139.html?qbl=relate_question_0&word=%C6%C6%CB%E9%BB%FA"
    url = "https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word=%B7%DB%CB%E9%BB%FA"
    spider=spider()
    spider.get_infos_url(url)
    # spider.get_infos_url(url1,url2,True)