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
import re
from mysql_class import Mysql
from google_translate_class import Googletranslate
class google:
    def __init__(self,mysql=None):
        self.mysql=mysql
        #循环终止标志
        self.flag=True
        self.start_time = time.time()
        self.currentLine=0
        self.mysqlNum=0  #插入数据库的数量
        self.mysqlrelation=0  #插入数据库的数量
        self.options = webdriver.ChromeOptions()
        # self.path="D:\\Anaconda3\\chromedriver.exe"
        self.path=r"D:\soft\python\chromedriver.exe"
        self.options.add_argument("user-data-dir=D:\data\scrapy" )
        # self.options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        self.options.binary_location = r"C:\Users\CYG\AppData\Local\Google\Chrome\Application\chrome.exe"
        # options.add_argument("--headless" )
        # self.browser = webdriver.Chrome(options=self.options, executable_path=self.path)
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
    def cut_keyword(self,keyword,maxlen=10):
        length=len(keyword)
        if length>maxlen:
            pass
            print(length,keyword)
            return length
        else:
            return keyword
    #通过浏览器进行翻译
    def translate_zh_en(self,data):
        try:
            inputbox=self.try_selector('tag',self.browser,'textarea')
            if inputbox:
                # print(data)
                return_data=''
                inputbox.send_keys(data)
                time.sleep(2)
                translate=self.try_selector('css',self.browser,'div.J0lOec')
                if translate:
                    # print(translate.text)
                    return_data=translate.text
                button=self.try_selector('css',self.browser,'button.GA2I6e')
                if button:
                    button.click()
                time.sleep(1)
                return str(return_data)
        except Exception as e:
            print(e)
            return False
    #打开浏览器-> 并且把翻译界面打开 ->调用数据库->循环翻译
    def get_infos_url(self,url):
        self.browser.get(url)
        tablename='zhidao_scrapy'
        while self.flag:
            all=self.mysql.table(tablename).where([{'translate':['=',0]}]).count()
            print(all)
            if all[0]==0:
                self.flag=False
                break
            res=self.mysql.table(tablename).field(['id','title','answer']).where([{'translate':['=',0]}]).limit(10).select()
            for line in res:
                translate=[]
                print('翻译id:{}的回答,翻译结果为:'.format(line[0]))
                translate.append({'title':self.translate_zh_en(line[1])})
                translate.append({'answer':self.translate_zh_en(line[2])})
                translate.append({'uid':line[0]})
                # print(translate)
                insert_flag=self.mysql.table('zhidao_scrapy_en').insert(translate)
                if insert_flag:
                    update_data = [{'translate':1}]
                    update_flag=self.mysql.table(tablename).where([{'id':['=',line[0]]}]).update(update_data)
                    if update_flag:
                        print('成功翻译插入数据并且更新数据库成功')
                    else:
                        print('成功翻译插入数据但是更新数据库失败')
                else:
                    print('翻译插入数据失败')
    #打开浏览器-> 并且把翻译界面打开 ->调用数据库->循环翻译
    def mysql_google_translate(self):
        tablename='zhidao_scrapy'
        google_object=Googletranslate()
        while self.flag:
            all=self.mysql.table(tablename).where([{'translate':['=',0]}]).count()
            print(all)
            if all[0]==0:
                self.flag=False
                break
            res=self.mysql.table(tablename).field(['id','title','answer']).where([{'translate':['=',0]}]).limit(10).select()
            for line in res:
                # print(line)
                translate=[]
                print('翻译id:{}的回答,翻译结果为:'.format(line[0]))
                translate.append({'title':google_object.googleTranslate(line[1])})
                # print('回答内容')
                # print(line[2])
                translate.append({'answer':google_object.googleTranslate(line[2])})
                translate.append({'uid':line[0]})
                # print(translate)
                insert_flag=self.mysql.table('zhidao_scrapy_en').insert(translate)
                if insert_flag:
                    update_data = [{'translate':1}]
                    update_flag=self.mysql.table(tablename).where([{'id':['=',line[0]]}]).update(update_data)
                    if update_flag:
                        print('成功翻译插入数据并且更新数据库成功')
                    else:
                        print('成功翻译插入数据但是更新数据库失败')
                else:
                    print('翻译插入数据失败')
    def filter_str(self,string1=''):
        # string1=string1.replace("\n",'<br/>')
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^（^）^(^)^:^,^.^。^-^%^!^?^\n]")  # 匹配不是中文、大小写、数字的其他字符
        string1 = cop.sub('',string1)
        return string1
if __name__=="__main__":
    mysql= Mysql()
    # print(mysql)
    google=google(mysql)
    # url='https://translate.google.com/?source=gtx'
    # google.get_infos_url(url)
    google.mysql_google_translate()
    # string1 = "@ad&*jfad张132（www）。()。,.\n。^&*%$#@?!"
    # print(string1)
    # result=google.filter_str(string1)
    # print(result)
