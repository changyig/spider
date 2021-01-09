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

    def filter_str(self,text=''):
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^（^）^(^)^:^,^.^。^-^%^!^?^\n]")  # 匹配不是中文、大小写、数字的其他字符
        text = cop.sub('',text)
        text = text.replace("\n",'<br/>').replace("-",'')
        return text
    def googleTranslate(self,text=''):
        """
            用谷歌翻译内容，返回翻译结果
            params: text 翻译的内容
            return: str s 翻译结果
        """
        try:
            text=self.filter_str(text)
            data = {
                'f.req':f'[[["MkEWBc","[[\\"{text}\\",\\"auto\\",\\"en\\",true],[null]]",null,"generic"]]]'
            }  # text则是你要翻译的内容
            res = requests.post(self.url,headers=self.headers,data=data).text  # 获取返回的结果
            # print(res)
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
        text = "破碎机有很多的类型，你找的破碎机的结构图，也会有不同的答案:这里我根据所了解到的类型来分别回答你的问题第一{}".format(i)
        print(text)
        text=google.googleTranslate(text)
        print(text)