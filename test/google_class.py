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
        self.records_text=''
        self.site=''
        self.next_href=''
        self.flag= True
        self.start_time = time.time()
        # 通过cursor执行增删查改
        options = webdriver.ChromeOptions()
        # path="D:\\Anaconda3\\chromedriver.exe"
        # path = r"D:\soft\anaconda\chromedriver.exe"
        path = r"D:\soft\python\chromedriver.exe"
        options.add_argument("user-data-dir=D:\data\scrapy" )
        # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        # options.add_argument("--headless" )
        options.binary_location = r"C:\Users\CYG\AppData\Local\Google\Chrome\Application\chrome.exe"
        self.browser = webdriver.Chrome(options=options, executable_path=path)
    def str_30_page(self,str=''):
        str='https://www.google.com/search?q=site:ag-susa.cz&sxsrf=ALeKk036e_EncQn8jCtxyJcz9NZ3afAibQ:1615597171494&ei=cw5MYMffHcrf-Qb82aaQCA&start=00&sa=N&ved=2ahUKEwiH5Ya8iKzvAhXKb94KHfysCYIQ8tMDegQIBhBL&biw=963&bih=937'
        res=str.split('&')
        res[3]='start=290'
        print('&'.join(res))
    def str_page(self,str=''):
        # res=str.split('&')
        # res[2]='start=290'
        # res='&'.join(res)
        cop = re.compile(r"&start=\d+")
        text = cop.sub('&start=290',str)
        return text
    def make_file(self,filename):
        if os.path.exists(filename):
            pass
            # with open('filename', mode='r', encoding='utf-8') as ff:
                # print(ff.readlines())
        else:
            with open(filename, mode='w', encoding='utf-8') as ff:
                print("文件创建成功！")
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
    def write_excel(self,path,nums,remark):
        # res = re.findall(r'\d+', content)
        # index = len(value)  # 获取需要写入数据的行数
        index = 1  # 获取需要写入数据的行数
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
        j = 0
        date=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        new_worksheet.write(0 + rows_old, j, self.site)  # 追加写入数据，注意是从i+rows_old行开始写入
        new_worksheet.write(0 + rows_old, j+1, nums)
        new_worksheet.write(0 + rows_old, j+2, remark)
        new_worksheet.write(0 + rows_old, j+3, date)
        new_workbook.save(path)  # 保存工作簿
        print('当前网站:{},site收录数量:{},收录信息:{},当前日期:{}'.format(self.site,nums,remark,date))

    def write_txt(self,keyword,filename):
        self.make_file(filename)
        with open(filename, "a", encoding='utf-8') as f:
            f.write(keyword+'\n')
    def pare_page_url2(self,count,url):
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
            # last_pages_text = self.browser.find_element_by_id('foot').find_elements_by_tag_name('td')[-2].text
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
    '''
        说明：获取30页的收录
    '''
    def page_30(self,url=''):
        self.browser.get(url)
        try:
            current_page = self.try_selector('xpath',self.browser,'//tr[@jsname="TeSSVd"]//td[@class="YyVfkd"]')
            if current_page:#含有30页
                print('含有30页')
                current_page=30
                pass
            else:#不包含30页
                print('不含有30页')
                current_page = self.try_selector('xpath',self.browser,'//tr[@jsname="TeSSVd"]//td[last()-1]').text
                self.records_num =int(current_page)*10
        except:
            try:
                robot = self.browser.find_element_by_id('captcha-form')
                if robot:
                    res = input('请输入y确认已经通过人机验证')
                    self.pare_page_url(1,url)
                    self.flag = True
            except:
                self.flag = False
                print('不含有30页')
                current_page = self.try_selector('xpath',self.browser,'//tr[@jsname="TeSSVd"]//td[last()-1]').text
                self.records_num = int(current_page) * 10

    '''
        说明：只保留数字 用来获取site收录的数量
    '''
    def get_digital(self,url=''):
        cop = re.compile(r"（.*）")
        url = cop.sub('',url)
        cop = re.compile("[^0-9]")
        text = cop.sub('',url)
        return int(text)

    '''
        说明：解析网页并获取网址的真实收录信息
    '''
    def pare_page_url(self,count,url):
        self.browser.get(url)
        try:
            self.records_text =self.try_selector('id',self.browser,'result-stats').text
            self.records_num = self.get_digital(str(self.records_text))
            print(self.records_num)
            current_page = self.try_selector('xpath',self.browser,'//tr[@jsname="TeSSVd"]//td[@class="YyVfkd"]')
            current_page_text = current_page.text
            next_pages = self.try_selector('xpath',self.browser,'//tr[@jsname="TeSSVd"]//td[@class="YyVfkd"]/following-sibling::td[1]/a[@href]')
            next_pages_href = next_pages.get_attribute("href")
            next_pages_href=self.str_page(next_pages_href)
            next_pages_text = next_pages.text
            print('当前页面:{}'.format(current_page_text))
            print('当前页面最后的a标签:{},a标签链接地址为:{}'.format(next_pages_text,next_pages_href))
            if self.records_num>=3000:
                self.page_30(next_pages_href)
                self.flag = False
            else:
                self.flag = False
        except Exception as e:
            print(e)
            try:
                robot = self.browser.find_element_by_id('captcha-form')
                if robot:
                    res = input('请输入y确认已经通过人机验证')
                    self.pare_page_url(count,url)
                    self.flag = True
            except:
                self.flag = False
                print('出现错误')
    #根据谷歌浏览器查看网站收录情况
    def pare_google_url(self,url):
        count=1
        self.next_href=url
        res=self.pare_page_url(count,self.next_href)
        while self.flag :
            time.sleep(3)
            count=count+1
            self.pare_page_url(count,self.next_href)
        self.write_excel(r'C:\Users\CYG\Desktop\data.xlsx',self.records_num,self.records_text)
if __name__=="__main__":
    # url="https://www.google.com.hk/search?q=site:am-lift.de"
    google = google()
    # google.str_30_page()
    with open(r"./txt/google_url.txt", 'r', encoding='utf-8') as infiles:
        lines=infiles.readlines()
        for line in lines:
            google.site=line
            url="https://www.google.com/search?q=site:{}".format(line)
            print(url)
            google.pare_google_url(url)
            time.sleep(10)
            # break
    url="https://www.google.com/search?q=site:salonikkrawiecki.pl&ei=praHX52VMYf7-Qb0ipS4DA&start=0&sa=N&ved=2ahUKEwidgKuWybXsAhWHfd4KHXQFBcc4HhDy0wN6BAgDEDM&biw=1261&bih=889"
    # google=google()
    # google.site='salonikkrawiecki.pl'
    # google.pare_google_url(url)