import selenium
import time
import hashlib
from selenium import webdriver
import os
import pymysql
from selenium.webdriver.chrome.options import Options
import re
class google:
    def __init__(self):
        self.connect = pymysql.connect(
            host="127.0.0.1",
            db="scrapy",
            user="root",
            passwd="root",
            charset='utf8',
            use_unicode=True
        )
        self.site=''
        self.next_href=''
        self.flag= True
        self.start_time = time.time()
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        options = webdriver.ChromeOptions()
        # path="D:\\Anaconda3\\chromedriver.exe"
        path = r"D:\soft\anaconda\chromedriver.exe"
        options.add_argument("user-data-dir=D:\data\scrapy" )
        # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        # options.add_argument("--headless" )
        options.binary_location = r"C:\Users\CYG\AppData\Local\Google\Chrome\Application\chrome.exe"
        self.browser = webdriver.Chrome(options=options, executable_path=path)

    def make_file(self,filename):
        if os.path.exists(filename):
            pass
            # with open('filename', mode='r', encoding='utf-8') as ff:
                # print(ff.readlines())
        else:
            with open(filename, mode='w', encoding='utf-8') as ff:
                print("文件创建成功！")
    def write_excel(self,content):
        print(content)
        res = re.findall(r'\d+', content)
    def write_txt(self,keyword,filename):
        self.make_file(filename)
        with open(filename, "a", encoding='utf-8') as f:
            f.write(keyword+'\n')
    def pare_page_url(self,url):
        self.browser.get(url)
        pnprev = self.browser.find_elements_by_xpath('//div[@id="foot"]//tr/td//a[@id="pnprev"]')
        if pnprev:
            current_page = self.browser.find_elements_by_xpath('//div[@id="foot"]//tr/td//span//parent::td')[0]
        else:
            current_page = self.browser.find_elements_by_xpath('//div[@id="foot"]//tr/td//span//parent::td')[1]
        current_page_text = current_page.text
        next_pages = self.browser.find_elements_by_xpath('//div[@id="foot"]//tr//a[@aria-label]')[-1]
        next_pages_href = next_pages.get_attribute("href")
        next_pages_text = next_pages.text
        last_pages_text = self.browser.find_element_by_id('foot').find_elements_by_tag_name('td')[-2].text
        print('当前页面:{}'.format(current_page_text))
        print('当前页面最后的a标签:{},a标签链接地址为:{}'.format(next_pages_text, next_pages_href))
        if current_page_text < next_pages_text:
            pass
        else:
            self.flag = False
        self.next_href=next_pages_href
        # return [current_page_text,next_pages_text,next_pages_href]
    #根据谷歌浏览器查看网站收录情况
    def pare_google_url(self,url):
        self.next_href=url
        res=self.pare_page_url(self.next_href)
        # print(res)
        while self.flag :
            time.sleep(5)
            self.pare_page_url(self.next_href)
        print('是最后一页')
        res_num = self.browser.find_element_by_id('result-stats').text
        self.write_excel(res_num)
        print(res_num)
if __name__=="__main__":
    # url="https://www.google.com.hk/search?q=site:am-lift.de"
    url="https://www.google.com/search?q=site:salonikkrawiecki.pl&ei=praHX52VMYf7-Qb0ipS4DA&start=0&sa=N&ved=2ahUKEwidgKuWybXsAhWHfd4KHXQFBcc4HhDy0wN6BAgDEDM&biw=1261&bih=889"
    google=google()
    google.site='salonikkrawiecki.pl'
    google.pare_google_url(url)