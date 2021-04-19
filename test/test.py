# coding:utf-8
from urllib import request,parse
import json
import requests
import os
import math
import pymssql
import difflib
import copy

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
def sql():
    insert_command="insert into google_keyword (keyword,result,list) values ('123',20,30)"
    connect = pymssql.connect('172.16.10.105','sa','sa','test')  #服务器名,账户,密码,数据库名
    conn = pymssql.connect(
        host='172.16.10.105',
        database='test',
        user='sa',
        password='sa'
    )
    cur = conn.cursor()
    cur.execute(insert_command)
    conn.commit()
    conn.close()
    print(conn)
    if connect:
        print("连接成功!")
    return connect
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
def compare_string():
    a='Used  Jaw crusher for the sale'
    b='used  Jaw crusher for the sale in indiz'
    a=stain_one_space(a)
    b=stain_one_space(b)
    # print(a)
    res=difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()
    print(res)
def test_site():
    str1='https://keatsteamympuls.nl/sitemap.xml'

if __name__ == '__main__':
    # res=download_img()
    compare_string()