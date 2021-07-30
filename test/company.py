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
from mysql_class import Mysql
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class mycompany:
    '''
    功能说明：通过谷歌查询收录 将结果存入道excel文件中
    self.site 访问的网站地址
    self.next_href 下一页地址
    self.records_num 收录的数量
    '''
    def __init__(self,mysql):
        self.mysql = mysql
        self.mysqlNum = 0  #插入数据库的数量
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
    def get_text_xpath(self,handle):
        try:
            handle.text
            # print(handle.text)
            return handle.text
        except Exception as e:
            print(e)
            return ''
    def get_text_xpath2(self,handle):
        try:
            # handle.get_attribute('value')
            # print(handle.get_attribute('value'))
            return handle.get_attribute('value')
        except Exception as e:
            print(e)
            return ''
    def get_page_content(self):
        table = self.try_selector('xpath',self.browser,'//table[@id="Content_Conn_GridView1"]')
        trs=self.try_selector('xpath',table,'//tr',True)
        # print(trs)
        data_list=[]

        for index,tr in enumerate(trs):
            if index>=1:
                # print(tr)
                data_dict = {}
                # print(index,self.get_text_xpath(self.try_selector('xpath',tr,'.//td[3]//p[1]')))
                data_dict['only_id']=int(self.get_text_xpath(self.try_selector('xpath',tr,'.//td[1]//p[1]')))
                data_dict['domain']=self.get_text_xpath(self.try_selector('xpath',tr,'.//td[3]//p[1]'))
                data_dict['origin']=self.get_text_xpath(self.try_selector('xpath',tr,'.//td[3]//p[3]'))
                data_dict['country']=self.get_text_xpath(self.try_selector('xpath',tr,'.//td[4]//p[2]'))
                data_dict['device']=self.get_text_xpath(self.try_selector('xpath',tr,'.//td[4]//p[5]'))
                data_dict['product']=self.get_text_xpath(self.try_selector('xpath',tr,'.//td[5]//p[1]'))
                data_dict['material']=self.get_text_xpath(self.try_selector('xpath',tr,'.//td[5]//p[2]'))
                data_dict['createtime']=self.get_text_xpath(self.try_selector('xpath',tr,'.//td[11]//p[1]'))
                data_dict['name']=self.get_text_xpath2(self.try_selector('xpath',tr,'.//td[13]//input[1]'))
                # print(data_dict)
                data_list.append(data_dict)
        #
        print(data_list)
        self.insert_mysql(data_list)
    '''
        说明：解析网页并获取网址的真实收录信息
    '''
    def login(self):
        self.browser.find_element_by_id("TextBox1").send_keys("liweidong")
        self.browser.find_element_by_id("TextBox2").send_keys("lwd123...")
        self.browser.find_element_by_id("Button1").click()
    def next_page(self,page=1):
        self.browser.find_element_by_id("ctl00$Content_Conn$AspNetPager1_input").clear()
        self.browser.find_element_by_id("ctl00$Content_Conn$AspNetPager1_input").send_keys(page)
        self.browser.find_element_by_id("ctl00$Content_Conn$AspNetPager1_btn").click()
        # time.sleep(5)
    def insert_mysql(self,data_list,tablename='company_swt2'):
        for data in data_list:
            try:
                insert_flag=insert_data=[{'only_id':data['only_id']},{'domain':data['domain']},{'origin':data['origin']},{'country':data['country']},{'device':data['device']},{'product':data['product']},{'material':data['material']},{'createtime':data['createtime']},{'name':data['name']}]
                if insert_flag:
                    self.mysql.table(tablename).insert(insert_data)
                    self.mysqlNum = self.mysqlNum + 1
                    print('主页面,问答页面h话题插入成功:{}，title:{},url:{}'.format(self.mysqlNum,data['domain'][0:10],data['material'][0:10]))
                else:
                    print('主页面,问答页面话题插入失败')
                    pass
            except BaseException as e:
                print("主页面或者问答页面话题相关性成功插入数据库的数量错误在这里>",e,"<错误在这里")
    def pare_page_url(self,url):
        self.browser.get(url)
        self.login()
        try:
            element = WebDriverWait(self.browser,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"menu"))
            )
            print('出现了menu')
            self.browser.get(url)
            for i in range(1,500):
                print('当前页面:{}'.format(i))
                self.next_page(i)
                self.get_page_content()
        finally:
            time.sleep(10)
            print('chuduol')
            self.browser.quit()




if __name__=="__main__":
    url="http://172.16.0.102:100/PhoneList.aspx?PhoneID=57"
    myql = Mysql()
    company=mycompany(myql)
    company.pare_page_url(url)