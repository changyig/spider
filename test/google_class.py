import selenium
import time
import hashlib
from selenium import webdriver
import os
import pymysql
from selenium.webdriver.chrome.options import Options
import re
import xlwt
import xlrd
from xlutils.copy import copy
class google:
    '''
    self.site 访问的网站地址
    self.next_href 下一页地址
    self.records_num 收录的数量
    '''
    def __init__(self):
        self.records_num=0
        self.site=''
        self.next_href=''
        self.flag= True
        self.start_time = time.time()
        # 通过cursor执行增删查改
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
    def write_excel(self,path,content):
        res = re.findall(r'\d+', content)
        # index = len(value)  # 获取需要写入数据的行数
        index = 1  # 获取需要写入数据的行数
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
        j = 0
        new_worksheet.write(0 + rows_old, j, self.site)  # 追加写入数据，注意是从i+rows_old行开始写入
        new_worksheet.write(0 + rows_old, j+1, res[0])
        new_worksheet.write(0 + rows_old, j+2, content)
        new_workbook.save(path)  # 保存工作簿

    def write_txt(self,keyword,filename):
        self.make_file(filename)
        with open(filename, "a", encoding='utf-8') as f:
            f.write(keyword+'\n')
    def pare_page_url(self,count,url):
        self.browser.get(url)
        try:
            if count ==1:
                self.records_num=self.browser.find_element_by_id('result-stats').text
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
                self.flag = True
            else:
                self.flag = False
                if int(current_page_text) <= 29:
                    self.records_num = self.browser.find_element_by_id('result-stats').text
            self.next_href=next_pages_href
        except:
            try:
                robot=self.browser.find_element_by_id('captcha-form')
                if robot:
                    res = input('请输入y确认已经通过人机验证')
                    self.pare_page_url(count, url)
                    self.flag = True
            except:
                self.flag = False
                print('出现错误')
        # return [current_page_text,next_pages_text,next_pages_href]
    #根据谷歌浏览器查看网站收录情况
    def pare_google_url(self,url):
        count=1
        self.next_href=url
        res=self.pare_page_url(count,self.next_href)
        while self.flag :
            time.sleep(3)
            count=count+1
            self.pare_page_url(count,self.next_href)
        print('是最后一页')
        self.write_excel(r'C:\Users\CYG\Desktop\data.xlsx',self.records_num)
        print(self.records_num)
if __name__=="__main__":
    # url="https://www.google.com.hk/search?q=site:am-lift.de"
    google = google()
    with open(r"./txt/google_url.txt", 'r', encoding='utf-8') as infiles:
        lines=infiles.readlines()
        for line in lines:
            google.site=line
            url="https://www.google.com/search?q=site:{}".format(line)
            print(url)
            google.pare_google_url(url)
    # url="https://www.google.com/search?q=site:salonikkrawiecki.pl&ei=praHX52VMYf7-Qb0ipS4DA&start=0&sa=N&ved=2ahUKEwidgKuWybXsAhWHfd4KHXQFBcc4HhDy0wN6BAgDEDM&biw=1261&bih=889"
    # google=google()
    # google.site='salonikkrawiecki.pl'
    # google.pare_google_url(url)