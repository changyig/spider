import selenium
import time
import hashlib
from selenium import webdriver
import os
import pymysql
from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
import time
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

    ##删除中断时txt文本中已经用过的关键词
    def del_txt(self):
        pass
    #解析从知道中获取的回答链接
    #注意流程：打开新的界面->切换成新的窗口句柄->抓取内容->关闭新窗口句柄->返回上一个窗口句柄
    def anwser_infos(self,url=''):
        cmd = 'window.open("'+url+'")'
        self.browser.execute_script(cmd)
        window = self.browser.window_handles
        self.browser.switch_to.window(window[1])
        # self.browser.maximize_window()
        article=self.browser.find_element_by_tag_name('article')
        title=self.try_selector('xpath',self.browser,'//h1[@accuse="qTitle"]')
        if title:
            title=title.text
        else:
            title =''
        if article:
            try:
                #判断是否含有隐藏的内容
                hide_content =self.try_selector('id',self.browser,"show-hide-container")
                if hide_content:
                    self.browser.execute_script("arguments[0].click();",hide_content)
                    # hide_content.click()
                else :
                    print('没有隐藏的内容')
                hide_content =self.try_selector('css',self.browser,"div.show-answer-dispute")
                if hide_content:
                    self.browser.execute_script("arguments[0].click();",hide_content)
                else :
                    print('没有隐藏的内容')
                answers =self.try_selector('css',article,".bd,.answer",True)
                i=1
                for answer in answers:
                    print("标题:{},第{}个人的回答,当前的链接地址:{}".format(title,i,url))
                    content=self.try_selector('css',answer,"div.answer-text")
                    if content:
                        answer_mask=self.try_selector('css',answer,"div.wgt-answers-mask")
                        if answer_mask:
                            self.browser.execute_script("arguments[0].click();",answer_mask)
                            # answer_mask.click()
                        print(content.text)
                    else:
                        print('.line.content div')
                        line=self.try_selector('css',answer,"div[class='line content'] div")
                        if line:
                            print(line.text)
                    i=i+1
            except Exception as e:
                print(e)
        self.browser.close()
        self.browser.switch_to.window(window[0])

    #输入关键词抓取内容
    def get_infos_url(self,keyword):
        self.browser.get(url)
        try:
            infos_container = self.browser.find_element_by_xpath('//div[@class="list-inner"]')
            foot_list = self.browser.find_element_by_xpath('//div[@class="list-footer"]')
            page_next = self.browser.find_element_by_xpath('//a[@class="pager-next"]')

            if infos_container:
                infos_list=infos_container.find_elements_by_tag_name('dl')
                for infos in infos_list:
                    title=infos.find_element_by_xpath('.//a')
                    a_url=title.get_attribute("href")
                    if a_url:
                        self.anwser_infos(a_url)
            #页面底部相关信息的链接 获取->存入数据库->下次调用
            if foot_list:
                pass

        except Exception as e:
            print(e)

    def try_css(self,handle='',element=''):
        try:
            content=handle.find_element_by_css_selector(element)
            return content
        except Exception as e:
            return False
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
            return False
    def get_url_info_from_queue(self):
       pass
if __name__=="__main__":
    keyword = '破碎机'
    url = "https://zhidao.baidu.com/search?ct=17&pn=0&tn=ikaslist&rn=10&fr=wwwt&ie=utf-8&word=%E7%A0%B4%E7%A2%8E%E6%9C%BA"
    spider=spider()
    spider.get_infos_url(url)