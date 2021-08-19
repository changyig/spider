# coding:utf-8
from urllib import request,parse
import json
import requests
import os
import math
import pymssql
import difflib
import copy
from lxml import etree
import re
import xlrd
import time
from xlutils.copy import copy
import json
def translate(content):
    url = "http://fanyi.baidu.com/sug"
    headers = {
        'User-Agent':'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10'
    }
    data = parse.urlencode({"kw":content})  # 将参数进行转码
    req = request.Request(url,data=bytes(data,encoding="utf-8"),headers=headers)
    r = request.urlopen(req)
    # print(r.code) 查看返回的状态码
    html = r.read().decode('utf-8')
    # json格式化
    html = json.loads(html)
    print(html)
    for k in html["data"]:
        print(k["k"],k["v"])
#将过长的内容按照，或者。分割符号进行均分，便于google翻译
def split_string(string='',maxlen=20):
    pattern='。'
    result_list=[]
    length=len(string)
    if length>maxlen:
        str_list=string.split(pattern)
        list_num=len(str_list)
        flag=True
        i=0
        temp=''
        while flag:
            temp_two=temp
            temp_two=temp_two+str_list[i]
            if len(temp_two)>maxlen:
                if i == list_num - 1:
                    result_list.append(temp)
                    result_list.append(str_list[i])
                else:
                    result_list.append(temp)
                    temp = str_list[i]
            else:
                if i==list_num-1:
                    result_list.append(temp_two)
                else:
                    if temp != '':
                        temp = temp + pattern + str_list[i]
                    else:
                        temp = temp + str_list[i]
            i = i + 1
            if i >= (list_num):
                flag = False
        return result_list
    else:
        return result_list.append(string)
def get_ip():
    url='http://api.shenlongip.com/ip?key=bblmg35e&pattern=json&count=1&need=1000&protocol=2'
    req =requests.get(url)
    data=json.loads(req.text)
    print(req.text)
    print(data)
    print(data['data'][0]['ip'])
    print(data['data'][0]['port'])
    proxy = {
        'http':'121.43.170.207:3128'
    }
    proxy2 = {
        'http':str(data['data'][0]['ip'])+':'+str(data['data'][0]['port'])
    }
    print(proxy2)
def download_img():
    for i in range(1,1000):
        url=r'https://osiedlewilanowka.pl/img/briquette machine/briquette_machine ('+str(i)+').jpg'
        response = requests.get(url)
        if response.status_code == 200:
            url_para=url.split('/')
            filename=url_para[-1]
            dir_path=url_para[-2]
            dir_path=r'C:\Users\CYG\Desktop/images/'+dir_path
            isDir=os.path.exists(dir_path)
            if not isDir:
                 os.mkdir(dir_path)
            isFile=os.path.exists(dir_path+'/'+filename)
            if not isFile:
                 with open(dir_path+'/'+filename, 'wb') as f:
                     print('链接地址：{},图片{}下载成功'.format(url,filename))
                     f.write(response.content)
            else:
                print('图片{}文件存在'.format(filename))
        else:
            print('不存在图片')
            break
'''
将txt里的内容分成等数量的多个txt文本
'''
def split_num_txt(self):
    filename=r'C:\Users\Administrator\Desktop\linshi.txt'
    with open(filename, mode='r', encoding='utf-8') as ff:
        txt1=ff.readlines()
        print(txt1)
        txt2=copy.deepcopy(txt1)
        for index,line in enumerate(txt1):
            txt2.pop(0)
            for index2,line2 in enumerate(txt2):
                print(index,line,index2,line2)
def stain_one_space(str=''):
    res=' '.join(str.split())
    return res
def combine_get_params(dicts):
    string=''
    for dict in dicts.items():
        if string=='':
            string+=str(dict[0])+'='+str(dict[1])
        else:
            string += '&'+str(dict[0]) + '=' + str(dict[1])
    string='?'+string
    return string
def filter_txt(text=''):
    pattern = re.compile("[^0-9^a-zA-Z^.^|^-]")
    text=pattern.sub('',text)
    return text
'''
说明:过滤掉多个空格只保留一个空格
'''
def stain_space(text=''):
    pattern = re.compile("\r\n")
    text = pattern.sub('',text)
    text=' '.join(text.split())
    return text
def write_exce(path,dicts):
    # res = re.findall(r'\d+', content)
    # index = len(value)  # 获取需要写入数据的行数
    index = 1  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path,formatting_info=True)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    j = 1
    date=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    new_worksheet.write(0 + rows_old, j, dicts['domain_name'])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_worksheet.write(0 + rows_old, j+2, dicts['ip'])
    new_worksheet.write(0 + rows_old, j+4, dicts['database_name'])
    new_worksheet.write(0 + rows_old, j+5, dicts['database_pwd'])
    new_worksheet.write(0 + rows_old, j+7, dicts['ftp_pwd'])
    new_workbook.save(path)  # 保存工作簿
    print(dicts['domain_name'],dicts['ip'],dicts['database_name'],dicts['database_pwd'],dicts['ftp_pwd'])
'''
说明：通过黑色后台url链接地址 获取最近分配的域名 并把它存入指定的excel文件中

'''
def get_domain_message(web_id,domain_name):
    headers = {
        'User-Agent':'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10'
    }
    cookies = {
        "CKFinder_Path":"Images%3A%2F%3A1",
        "SEOCack":"b4Pb1fUCj8Nl8cz/A7kRascI5PBDd+zNjItKAqXB92+X4ZxgL6uqdFWWEXQunGl6b1315AdbsgkU35kNaEAzwCoCTlC9tQGs4slh9E4L0YTG0FLJPx90rioF5WjIDzUi",

    }
    url='http://172.16.10.90:88/!admin/List-WebDetails.aspx'
    dict = {'WebId':web_id,'webname':domain_name}
    url = url + combine_get_params(dict)
    print(url)
    html = requests.get(url,headers=headers,cookies=cookies)
    print(html)
    if html.status_code == 200:
        try:
            ip = etree.HTML(html.content).xpath("//input[@id='ctl00_main_TextBox_WIP']/@value")[0]
            name = etree.HTML(html.content).xpath("//input[@id='ctl00_main_TextBox_WFTPUser']/@value")[0]
            pwd = etree.HTML(html.content).xpath("//input[@id='ctl00_main_TextBox_WFTPPwd']/@value")[0]
            database = etree.HTML(html.content).xpath("//textarea[@id='ctl00_main_TextBox_WFTPConn']")[0].xpath('string(.)')
            database = stain_space(database)
            print(ip,name,pwd,database)
            return ip,name,pwd,database
        except Exception as e:
            print(e)
            print('域名ftp信息尚未填写，确认后在尝试获取')
            return False
        # ip_text = ip.xpath('string(.)')
        # print(ip_text)
def get_message():
    url='http://172.16.10.90:88/!admin/List-WebStatus.aspx'
    headers = {
        'User-Agent':'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10'
    }
    cookies = {
        "CKFinder_Path":"Images%3A%2F%3A1",
        "SEOCack":"b4Pb1fUCj8Nl8cz/A7kRascI5PBDd+zNjItKAqXB92+X4ZxgL6uqdFWWEXQunGl6b1315AdbsgkU35kNaEAzwCoCTlC9tQGs4slh9E4L0YTG0FLJPx90rioF5WjIDzUi",

    }
    dict={'kfuserid':626,'IndustryID':0,'SclassID':0,'Show':'','Wtags':'','Host':'','zuhe':0,'order':'desc'}
    url=url+combine_get_params(dict)

    html=requests.get(url,headers=headers,cookies=cookies)
    filename=r'C:\Users\CYG\Desktop\test.html'
    if html.status_code == 200:
        with open(filename,'wb') as f:
            f.write(html.content)
        dicts={'domain_name':'','web_id':'','ip':'','ftp_name':'','ftp_pwd':'','database_name':'','database_pwd':''}
        tr=2
        td_id=etree.HTML(html.content).xpath("//table[@id='ctl00_main_GridView1']//tr[{}]//td[1]".format(tr))[0]
        # td_id_text = etree.tostring(td_id,method='html')
        td_id_text = td_id.xpath('string(.)')
        td_domain = etree.HTML(html.content).xpath("//table[@id='ctl00_main_GridView1']//tr[{}]//td[7]".format(tr))[0]
        td_domain_text = td_domain.xpath('string(.)')
        td_id_text= filter_txt(td_id_text)
        td_domain_text=filter_txt(td_domain_text)
        web_id=td_id_text.split('|')[1]
        domain_name=td_domain_text.split('|')[0]
        print(web_id,domain_name)
        res=get_domain_message(web_id,domain_name)
        if res:
            dicts['domain_name'],dicts['web_id'],dicts['ip'],dicts['ftp_name'],dicts['ftp_pwd'],dicts['database_name'],dicts['database_pwd']=\
            domain_name,web_id,res[0],res[1],res[2],res[3].split(' ')[0],res[3].split(' ')[1]
            print(dicts)
            path=r'E:\红星办公文件\xls表格文档\域名分配\域名分配.xlsx'
            write_exce(path,dicts)
    # print(html)
'''
查询网站信息
'''
def read_txt_cookie():
    data_dict={}
    with open('./txt/cookie.txt','r') as f:
        data=f.read().split(';')
        for i in data:
            cookie_item=i.split('=')
            data_dict[cookie_item[0].strip()]=cookie_item[1].strip()
    return data_dict
# import flask
# from flask import Flask
# # 实例化，可视为固定格式
# app = Flask(__name__)
#
# @app.route('/getmsg')
def query_msg():
    pass
    # url = flask.request.args.get("url")
    # print(url)
    # url = 'https://baidurank.aizhan.com/baidu/163.com/'
    # url = 'http://172.16.10.101:8080/index.php/home/test2017/get_headers'
    # headers = {
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    #     # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    #
    # }
    # cookies = {
    #     "Hm_lvt_b37205f3f69d03924c5447d020c09192":"1625555582",
    #     "allSites":"163.com%2C0",
    #     "Hm_lvt_de25093e6a5cdf8483c90fc9a2e2c61b":"1625565477",
    #     "Hm_lpvt_de25093e6a5cdf8483c90fc9a2e2c61b":"1625565477",
    #     "_csrf":"df5794697f4b2e4a5c273edf46707c25649705667845a96dc3e5473de903ba38a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22pUjom6_Jtq92Z7QceqDSGk-oXVy2QE7e%22%3B%7D",
    #     "Hm_lpvt_b37205f3f69d03924c5447d020c09192":"1625618736",
    #
    # }
    # cookies = read_txt_cookie()
    # # print(cookies)
    # html = requests.get(url,headers=headers,cookies=cookies)
    # filename = r'C:\Users\CYG\Desktop\test.html'
    # data_dict=[]
    # if html.status_code == 200:
    #     with open(filename,'wb') as f:
    #         f.write(html.content)
    #     res=etree.HTML(html.content).xpath("//td[@class='title']")
    #     for index, td in enumerate(res):
    #         if index !=0:
    #             data_dict.append(''.join(td.xpath('string(.)').split()))
    # return json.dumps(data_dict)
if __name__ == '__main__':
    # res=download_img()
    get_message()
    # app.run(host="0.0.0.0", port=5000)