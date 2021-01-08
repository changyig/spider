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
class google:
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
        self.path="D:\\Anaconda3\\chromedriver.exe"
        # self.path=r"D:\soft\python\chromedriver.exe"
        self.options.add_argument("user-data-dir=D:\data\scrapy" )
        self.options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        # self.options.binary_location = r"C:\Users\CYG\AppData\Local\Google\Chrome\Application\chrome.exe"
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
    def cut_keyword(self,keyword,maxlen=200):
        length=len(keyword)
        if length>maxlen:
            pass
    def get_infos_url(self,url):
        self.browser.get(url)
        keyword="想要购买锯末粉碎机建找一个权威的企业去咨询，正远粉体这家品牌的粉碎机很受大家欢迎挑选粉碎机重要的是选一个专业的厂家根据需求去选择。粉碎机在粉碎过程中施加于物料的外力有压轧、 晶体粉碎机刀组 剪切、冲击（打击）、研磨四种。压轧主要用在粗、中碎，适用于硬质料和大块料的破碎；剪切主要用在破碎或粉碎，适于韧性或纤维性物料的粉碎。潍坊正远粉体工程设备有限公司是一家集超微粉体设备的研制、开发、试验、生产、销售和服务为一体的综合性高新技术企业"
        inputbox=self.try_selector('tag',self.browser,'textarea')
        for i in range(100):
            print(i)
            if inputbox:
                print(inputbox)
                inputbox.send_keys(keyword)
                time.sleep(2)
                translate=self.try_selector('css',self.browser,'div.J0lOec')
                if translate:
                    print(translate.text)
                button=self.try_selector('css',self.browser,'button.GA2I6e')
                time.sleep(2)
                if button:
                    button.click()



if __name__=="__main__":

    google=google()
    str='https://translate.google.com/?source=gtx'
    google.get_infos_url(str)