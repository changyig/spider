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
import urllib
import sys
import re
from mysql_class import Mysql
class spider:
    def __init__(self,mysql):
        self.mysql=mysql
        #验证码不正确时一直输入验证码
        self.flag=True
        self.start_time = time.time()
        self.currentLine=0
        self.currentPage=0 #主页面当前页码
        self.secondPage = 1 #问答页面当前页码
        self.pattern='破.*机|矿山|粉.*机|砂机|磨.*机|破.*碎'
        self.keyword='破.*机|矿山|粉.*机|砂机'

        self.mysqlNum=0  #插入数据库的数量
        self.mysqlrelation=0  #插入数据库的数量
        # 通过cursor执行增删查改
        # self.cursor = self.connect.cursor()
        self.options = webdriver.ChromeOptions()
        # self.path="D:\\Anaconda3\\chromedriver.exe"
        self.path=r"D:\soft\python\chromedriver.exe"
        self.options.add_argument("user-data-dir=D:\data\scrapy" )
        # self.options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.options.binary_location = r"C:\Users\CYG\AppData\Local\Google\Chrome\Application\chrome.exe"
        # self.options.add_argument("--headless" )
        self.browser = webdriver.Chrome(options=self.options, executable_path=self.path)
        #隐形等待
        # self.browser.implicitly_wait(10)

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
    def md5_str_onlyid(self,data=None):
        try:
            url=data['url']
            url=url.split('?')
            str_md5=(url[0]+str(data['page'])+str(data['author'])).encode(encoding='UTF-8')
            str_md5= hashlib.md5(str_md5).hexdigest()
            return str_md5
        except Exception as e:
            print(e)
            return 'error'
    #判断主页面的url和标题是否和主关键词相关，重复返回False 不重复返回True
    def check_onlyid(self,url='',title=''):
        try:
            match=re.search(self.pattern,title)
            if match is None:
                print('内容不相关跳过:{},'.format(title))
                return False
            else:
                # url=url.split('?')
                # str_md5=(url[0]+str(1)).encode(encoding='UTF-8')
                str_md5=(url+str(1)).encode(encoding='UTF-8')
                str_md5= hashlib.md5(str_md5).hexdigest()
                where_data=[{'onlyid':['=',str(str_md5)]}]
                find=self.mysql.table('zhidao_scrapy').field(['id','onlyid']).where(where_data).find()
                if find:
                    print('地址重复跳过:{},数据库id:{}'.format(url[0],find[0]))
                    return False
                else:
                    return True
        except Exception as e:
            print(e)
            return True
    ##问答页内容的数据存入到数据库 : 抓取到的问答页面->解析和过滤数据->存入数据库（数据唯一性判断）
    def answer_insert_mysql(self,data,tablename='zhidao_scrapy'):
        onlyid=self.md5_str_onlyid(data)
        try:
            insert_data=[{'keyword':data['title']},{'title':data['title']},{'answer':data['content']},{'url':data['url']},{'onlyid':onlyid},{'date':data['date']},{'page':data['page']},{'ranking':data['author']}]
            self.mysql.table(tablename).insert(insert_data)
            self.mysqlNum = self.mysqlNum + 1
            # print('问答页面成功插入数据库的数量:{},title:{}'.format(self.mysqlNum,data['title']))
            print('问答页面成功插入数据库的数量:{},title:{},内容：{}'.format(self.mysqlNum,data['title'][0:20],data['content'][0:20]))
        except BaseException as e:
            print("问答页面错误在这里>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<错误在这里")
        pass

    ##相关性标题的数据存入到数据库 : 抓取到主页面相关问题->解析和过滤数据->存入数据库（数据唯一性判断）
    def relation_insert_mysql(self,data,tablename='zhidao_relation'):
        try:
            insert_flag=insert_data=[{'keyword':data['title']},{'title':data['title']},{'url':data['url']},{'origin':data['origin']},{'date':data['date']}]
            if insert_flag:
                self.mysql.table(tablename).insert(insert_data)
                self.mysqlNum = self.mysqlNum + 1
                self.mysqlrelation = self.mysqlrelation + 1
                print('主页面,问答页面h话题插入成功:{}，title:{},url:{}'.format(self.mysqlrelation,data['title'][0:10],data['url'][33:70]))
            else:
                print('主页面,问答页面话题插入失败')
                pass
        except BaseException as e:
            print("主页面或者问答页面话题相关性成功插入数据库的数量错误在这里>",e,"<错误在这里")

    ##处理获取到url链接地址
    def filter_url(self,url):
        res = url.split("'")
        return res[-2]

    #获取问答页面下的相关性问题 问答->相关标题
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
        cmd = 'window.open("' + url + '")'
        self.browser.execute_script(cmd)
        window = self.browser.window_handles
        self.browser.switch_to.window(window[1])
        time.sleep(1)
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
                #判断当前问答页的页码
                self.current_second_page()
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
                        line = self.try_selector('css',answer,"div[class='line content'] div")
                        if line:
                            # print(line.text)
                            data_content = line.text
                    data = {}
                    data['title'] = title
                    data['author'] = i
                    data['content'] = data_content
                    data['url'] = url
                    data['page'] = self.secondPage
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
                    self.secondPage=int(self.secondPage)+1
                    print('下一页链接地址:{}'.format(next_page_url))
                    self.browser.close()
                    self.browser.switch_to.window(window[0])
                    self.anwser_infos(next_page_url)
                else:
                    self.browser.close()
                    self.browser.switch_to.window(window[0])
            except Exception as e:
                self.browser.close()
                self.browser.switch_to.window(window[0])
                print(e)
        else:
            self.browser.close()
            self.browser.switch_to.window(window[0])
            print('没有找到相关性的文章')

    #判断主界面的的当前页面 默认为零
    def current_page(self):
        page = self.try_selector('css',self.browser,'div.pager')
        if page:
            b = page.find_element_by_tag_name('b')
            if b:
                self.currentPage = int(b.text)
    #判断问答页当前页面 默认为零
    def current_second_page(self):
        page=self.try_selector('css',self.browser,'div.pager')
        if page:
            b=page.find_element_by_tag_name('b')
            if b:
                self.secondPage=int(b.text)

    #根据关键词抓取主的内容
    def get_infos_url(self,url,url2='',flag=False):
        self.browser.execute_script("window.location.href = '{}';".format(url))
        self.current_page()
        print('主页面当前页面页码是：{}'.format(self.currentPage))
        if flag and url2:
            self.browser.execute_script("window.location.href = '{}';".format(url2))
        try:
            infos_container = self.try_selector('xpath',self.browser,'//div[@class="list-inner"]')
            if infos_container:
                infos_list=infos_container.find_elements_by_tag_name('dl')
                for infos in infos_list:
                    title=infos.find_element_by_xpath('.//a')
                    a_url=title.get_attribute("href")
                    a_title=title.text
                    if a_url and a_title:
                        res=self.check_onlyid(a_url,a_title)
                        if res:
                            print('bu跳过')
                            self.anwser_infos(a_url)
                        else:
                            print('跳过')
            #页面底部相关信息的链接 获取->存入数据库->下次调用
            foot_list = self.try_selector('xpath',self.browser,'//div[@class="list-footer"]')
            if foot_list:
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
    def main(self):
        tablename='zhidao_relation'
        while self.flag:
            find=self.mysql.table(tablename).field(['id','keyword']).where([{'count':['=',0]}]).find()
            print(find)
            if find:
                keyword=find[1]
                keyword=urllib.parse.quote(keyword,encoding="gbk")
                url="https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&ie=gbk&word={}".format(keyword)
                print('主页面当前关键词:{},url链接地址：{}'.format(find[1],url))
                spider.get_infos_url(url)
                update_data=[{'count':1}]
                update_flag=self.mysql.table(tablename).where([{'id':['=',find[0]]}]).update(update_data)
                update_flag=self.mysql.table(tablename).where([{'count':['=',0]},{'keyword':['not like','破%机']}]).where([{'keyword':['not like','破%碎']}]).update([{'count':3}])
if __name__=="__main__":
    myql=Mysql()
    spider=spider(myql)

    keyword =spider.main()
    # url2 = "https://zhidao.baidu.com/search?word=%C6%C6%CB%E9%BB%FA%D3%D0%C4%C4%D0%A9%D6%D6%C0%E0&ie=gbk&site=-1&sites=0&date=0&pn=100"
    # url1 = "https://zhidao.baidu.com/question/1430633872239462139.html?qbl=relate_question_0&word=%C6%C6%CB%E9%BB%FA"
    # url = "https://zhidao.baidu.com/search?ct=17&pn=0&tn=ikaslist&rn=10&fr=wwwt&ie=utf-8&word=%E8%B4%AD%E4%B9%B0%E7%A0%B4%E7%A2%8E%E6%9C%BA%E6%B3%A8%E6%84%8F%E7%9A%84%E9%97%AE%E9%A2%98"
    # spider.get_infos_url(url)
    # spider.md5_str_onlyid()
    # spider.get_infos_url(url1,url2,True)
