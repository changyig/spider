# coding:utf-8
import requests
import json
import re
import time

class Googletranslate:
    def __init__(self):
        self.lang = 'en'
        self.url = 'https://translate.google.cn/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&f.sid=-2984828793698248690&bl=boq_translate-webserver_20201221.17_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=5445720&rt=c'
        self.headers = {
            'origin'        :'https://translate.google.cn',
            'referer'       :'https://translate.google.cn/',
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-origin',
            'user-agent'    :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'x-client-data' :'CIW2yQEIpbbJAQjEtskBCKmdygEIrMfKAQj2x8oBCPfHygEItMvKAQihz8oBCNzVygEIi5nLAQjBnMsB',
            'Decoded'       :'message ClientVariations {repeated int32 variation_id = [3300101, 3300133, 3300164, 3313321, 3318700, 3318774, 3318775, 3319220, 3319713, 3320540, 3329163, 3329601];}',
            'x-same-domain' :'1'
        }
    #将超出字符串指定长度自动截取，并返回结果
    def split_string(self,string='',maxlen=5000):
        pattern = ','
        result_list = []
        length = len(string)
        if length > maxlen:
            str_list = string.split(pattern)
            list_num = len(str_list)
            flag = True
            i = 0
            temp = ''
            while flag:
                temp_two = temp
                temp_two = temp_two + str_list[i]
                if len(temp_two) > maxlen:
                    if i == list_num - 1:
                        result_list.append(temp)
                        result_list.append(str_list[i])
                    else:
                        result_list.append(temp)
                        temp = str_list[i]
                else:
                    if i == list_num - 1:
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
            result_list.append(string)
            return result_list
    def filter_str(self,text=''):
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^（^）^(^)^:^,^.^。^，^-^%^!^?^\n]")  # 匹配不是中文、大小写、数字的其他字符
        text = cop.sub('',text)
        text = text.replace("\n",'<br/>').replace("-",'').replace('，',',').replace('。','.')
        return text
    def googleTranslateText(self,text=''):
        data = {
            'f.req':f'[[["MkEWBc","[[\\"{text}\\",\\"auto\\",\\"en\\",true],[null]]",null,"generic"]]]'
        }  # text则是你要翻译的内容
        try:
            res = requests.post(self.url,headers=self.headers,data=data,proxies={'https':'49.69.202.80:35872'},timeout=3)  # 获取返回的结果
        except Exception as e:
            print('超时出现了')
            return None
        # print(res.status_code)
        res = res.text
        pattern = '\)\]\}\'\s*\d{3,5}\s*\[(.*)\s*'  # 提取需要的部分
        part1 = re.findall(pattern,res)
        part1_list = json.loads(part1[0])  # 字符串转列表
        if part1_list[2] is None:  # 如果返回的结果中没有需要的数据，则返回输入的内容
            return None
        content1 = part1_list[2].replace('\n','')
        part2_list = json.loads(content1)[1][0][0][5:][0]  # 过滤结果中重复的部分
        s = ''
        for i in part2_list:  # 遍历结果中的每一句话，并进行拼接
            s += i[0]
        return s
    def googleTranslate2(self,text=''):
        """
            用谷歌翻译内容，返回翻译结果
            params: text 翻译的内容
            return: str s 翻译结果
        """
        try:
            return_str=''
            text=self.filter_str(text)
            res_list=self.split_string(text)
            for list in res_list:
                res_str=self.googleTranslateText(list)
                if res_str is None:
                    print('翻译出错了2')
                    return ''
                else:
                    return_str=return_str+'.'+res_str
            return return_str.lstrip('.')
        except Exception as e:
            print('翻译出错了1')
            print(e)
            return ''
    def googleTranslate(self,text=''):
        """
            用谷歌翻译内容，返回翻译结果
            params: text 翻译的内容
            return: str s 翻译结果
        """
        try:
            text=self.filter_str(text)
            # print(text)
            data = {
                'f.req':f'[[["MkEWBc","[[\\"{text}\\",\\"auto\\",\\"en\\",true],[null]]",null,"generic"]]]'
            }  # text则是你要翻译的内容
            try:
                res = requests.post(self.url,headers=self.headers,data=data,timeout=3)  # 获取返回的结果
            except Exception as e:
                print('超时出现了')
                return None
            # print(res.status_code)
            res=res.text
            pattern = '\)\]\}\'\s*\d{3,5}\s*\[(.*)\s*'  # 提取需要的部分
            part1 = re.findall(pattern,res)
            part1_list = json.loads(part1[0])  # 字符串转列表
            if part1_list[2] is None:  # 如果返回的结果中没有需要的数据，则返回输入的内容
                return text
            content1 = part1_list[2].replace('\n','')
            part2_list = json.loads(content1)[1][0][0][5:][0]  # 过滤结果中重复的部分
            s = ''
            for i in part2_list:  # 遍历结果中的每一句话，并进行拼接
                s += i[0]
            return s
        except Exception as e:
            print('翻译出错了')
            print(e)
            return ''
if __name__=="__main__":
    pass
    google=Googletranslate()
    for i in range(1):
        text = '可逆式制砂机的工作原理是电动机通过皮带传动带动转子旋转，使转子盘上的锤头高速旋转，当物料进入破碎腔时，受到高速旋转锤头的冲击而破碎，并被冲击到反击区，再次进行破碎，另外部分被冲击的石料在运动中撞击到下落的物料，同时进行破碎。这样多次反复冲击、反击、撞击，最终物料形成小颗粒通过锤头和破碎板之间的间隙而排出。'
        print(text)
        text=google.googleTranslate2(text)
        print(text)