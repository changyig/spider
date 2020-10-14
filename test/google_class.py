import selenium
import time
import hashlib
from selenium import webdriver
import os
import pymysql
from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
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
        self.start_time = time.time()
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        options = webdriver.ChromeOptions()
        path="D:\\Anaconda3\\chromedriver.exe"
        options.add_argument("user-data-dir=D:\data\scrapy" )
        options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        # options.add_argument("--headless" )
        self.browser = webdriver.Chrome(options=options, executable_path=path)

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
    #解析从搜狐引擎中获取到的列表元素并将（标题，内容，关键词，=》存入数据中）
    def pare_google_url(self,url):
        self.browser.get(url)
        res_num = self.browser.find_element_by_id('result-stats').text
        next_page=self.browser.find_element_by_id('foot').text
        # pages=self.browser.find_element_by_id('foot').find_element_by_tag_name('tr')
        pages=self.browser.find_elements_by_xpath('//div[@id="foot"]//tr//a[@aria-label]')[-1].get_attribute("href")
        last_pages=self.browser.find_element_by_id('foot').find_elements_by_tag_name('td')[-1].text
        print(next_page)
        print(pages)
        print(last_pages)

if __name__=="__main__":
    # url="https://www.google.com/search?q=site%3Asalonikkrawiecki.pl&oq=site%3Asalonikkrawiecki.pl&aqs=chrome..69i57j69i58.3599j0j1&sourceid=chrome&ie=UTF-8"
    url="https://www.google.com/search?q=site%3Asalonikkrawiecki.pl&oq=site%3Asalonikkrawiecki.pl&aqs=chrome..1571&sourceid=chrome&ie=UTF-8"
    google=google()
    google.pare_google_url(url)