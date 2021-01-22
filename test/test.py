# coding:utf-8
from urllib import request,parse
import json
import requests
import math

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
if __name__ == '__main__':
    res=get_ip()
