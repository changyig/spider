from bs4 import BeautifulSoup
import requests
from mysql_class import Mysql
# from urllib3 import request
import urllib3
import os
import datetime
import time
from lxml import etree
from dateutil.relativedelta import *

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
# r = requests.get(url, headers=headers, cookies=cookies)
# soup = BeautifulSoup(content,"html.parser")
def write_keyword(keyword):
    with open("./url.txt","a",encoding='utf-8') as f:
        f.write(keyword+'\n')
def write_filename_keyword(filename,keyword):
    with open(filename,"a",encoding='utf-8') as f:
        f.write(keyword+'\n')
def read_url():
    url = 'https://www.fruitfuler.com/sitemap.xml'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "xml")
    count = soup.find_all(name="loc")
    num = 0
    for i in count:
        url_text=i.string
        res = requests.get(url_text)
        soup2 = BeautifulSoup(res.text, "xml")
        keyword_url = soup2.find_all(name="loc")
        for word in keyword_url:
            keyword=word.string
            if keyword.find('.html')>0:
                # print(keyword)
                write_keyword(keyword)
'''
说明:从含有关键词的url中提取关键词
'''
def test(url):
    path1 = url.split('/')[-1]
    str_list=path1.replace('.html','').split('-')
    str=' '.join(str_list)
    write_filename_keyword('./keyword.txt',str)
'''
说明:访问网站站点地图，爬取含有完整关键词的url 并存入txt文本中
'''
def read_url_keyword():
    url = 'https://www.capriccio-music.de/sitemap.xml'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "xml")
    count = soup.find_all(name="loc")
    num = 0
    for i in count:
        url_text=i.string
        res = requests.get(url_text)
        soup2 = BeautifulSoup(res.text, "xml")
        keyword_url = soup2.find_all(name="loc")
        for word in keyword_url:
            keyword=word.string
            if keyword.find('.html')>0:
                test(keyword)
                # write_keyword(keyword)
# read_url_keyword()
def read_keyword(url):
    content = requests.get(url,headers=headers)
    # http = urllib3.https
    # content = http.request('GET', url)
    print(content)
    # soup = BeautifulSoup(content.text, "html.parser")
    # print(soup)
def process_url():
    f=open('url.txt','r',encoding="utf-8")
    for i in range(10):
        url=f.readline()
        read_keyword(url)
        print(i)
        print(url)
        break
# 字符串格式转换成 2020-02-03 11:05:03
def time_transform(date):
    try:
        time_stamp=time.mktime(time.strptime(date,"%Y-%m-%d"))
        struct_time = time.localtime(time_stamp)  # 得到结构化时间格式
        now_time = time.strftime("%Y-%m-%d %H:%M:%S",struct_time)
        # print(now_time)
        return now_time
    except Exception as e:
        return '00-00-00 00:00:00'
'''
返回以每个月为一组的列表
eg:[{'starttime': '2018-01-01', 'endtime': '2018-01-31'}, {'starttime': '2018-02-01', 'endtime': '2018-02-28'}]
'''
def loop_date(starttime='2018-01-01',data=[]):
    timestamp=int(time.mktime(time.strptime(starttime,"%Y-%m-%d")))
    now=int(time.time())
    if timestamp<now:
        dict_data={}
        endtime = (datetime.datetime.strptime(starttime,"%Y-%m-%d") + relativedelta(months=+1) - relativedelta(
            minutes=+1)).strftime("%Y-%m-%d")
        temptime = (datetime.datetime.strptime(starttime,"%Y-%m-%d") + relativedelta(months=+1)).strftime("%Y-%m-%d")
        dict_data['starttime']=starttime
        dict_data['endtime']=endtime
        data.append(dict_data)
        loop_date(starttime=temptime,data=data)
        return data
    else:
        return data
'''
说明：通过接口获取后台数据的询盘信息
'''
def test_url():
    time_list=loop_date()
    for list in time_list:
        data={}
        url='http://172.16.0.121:807/index.php/index/longword_liebiao'
        data['starttime']=list['starttime']
        data['endtime']=list['endtime']
        get_data=''
        for item in data.items():
            if get_data =='':
                get_data=get_data+item[0]+'='+item[1]
            else:
                get_data = get_data +'&' + item[0] + '=' + item[1]
        url=url+'?'+get_data
        print(url)
        r = requests.get(url,headers=headers)
        res=r.json()
        # print(res)
        mysql = Mysql()
        try:
            for dict_one in res:
                insert_data=[]
                insert_data.append({'person':dict_one['remark1']})
                insert_data.append({'web':dict_one['host']})
                insert_data.append({'url':dict_one['url']})
                insert_data.append({'country':dict_one['area']})
                insert_data.append({'product':dict_one['key']})
                insert_data.append({'inquiry_date':dict_one['datetime']})
                insert_data.append({'online_date':time_transform(dict_one['online_time'])})
                insert_data.append({'starttime':data['starttime']})
                insert_data.append({'endtime':data['endtime']})
                mysql.table('inquiry').insert(insert_data)
        except Exception as e:
            print(e)
# test_url()
def url_title(url=''):
    try:
        keyword_html=requests.get(url)
        if keyword_html.status_code ==200:
            keyword = BeautifulSoup(keyword_html.text,"html.parser")
            title = keyword.title.string
        else:
            title=''
        return title
    except Exception as e:
        return ''
'''
说明:读取询盘表中数据 根据数据url更新 title字段
'''
def read_mysql_update_title():
    pass
    mysql = Mysql()
    where=[{'url':['!=','']},{'title':['=','']}]
    # urls=mysql.table('inquiry').field(['id','title','url']).where(where).limit(3).select()
    urls=mysql.table('inquiry').field(['id','title','url']).where(where).select()
    for url in urls:
        print(url[2])
        res=url_title(url[2])
        print(res)
# read_mysql_update_title()
# data=loop_date()
# print(data)
# time_transform('2019-12-20')

def write_sitemap():
    url = 'https://www.transports-speciaux.ch/sitemap.xml'
    filename='./sitemap_url.txt'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "xml")
    count = soup.find_all(name="loc")
    num = 0
    for i in count:
        url_text = i.string
        res = requests.get(url_text,headers=headers)
        soup2 = BeautifulSoup(res.text, "xml")
        keyword_url = soup2.find_all(name="loc")
        for word in keyword_url:
            print(word)
            keyword = word.string
            write_filename_keyword(filename,keyword)


def write_html():
    str1='aaaa'
    with open(r'C:\Users\CYG\Desktop\test.html',mode='w',encoding='utf-8') as f:
        f.write('aaaa')
def read_html():
    with open(r'C:\Users\CYG\Desktop\test.html',mode='r',encoding='utf8') as f:
        html=f.read()
        # print(html)
        # print(f.read())
        tree = etree.HTML(html)
        try:
            keyword_alist=[]
            a_list = tree.xpath("//div[@id='bres']//a")
            print(a_list)
            for a in a_list:
                print(a)
                keyword_alist.append(a.xpath("string()"))#注意区分a.xpath("//text()")
                print(keyword_alist)
            return keyword_alist
        except Exception as e:
            print(e)
            return []
read_html()
# write_sitemap()