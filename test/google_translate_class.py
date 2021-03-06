# coding:utf-8
import requests
import json
import re
import time
'''
google翻译接口
'''
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
    '''
    将特殊字符进行过滤掉，并返回过滤后的结果
    '''
    def filter_str(self,text=''):
        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9^（^）^(^)^:^,^.^。^，^%^!^?^\n^×^、^\-^<^>^=^/^～]")  # 匹配不是中文、大小写、数字的其他字符
        text = cop.sub('',text)
        text = text.replace("\n",'<br/>').replace('，',',').replace('。','.')
        return text
    def googleTranslateText(self,text=''):
        data = {
            'f.req':f'[[["MkEWBc","[[\\"{text}\\",\\"auto\\",\\"en\\",true],[null]]",null,"generic"]]]'
        }  # text则是你要翻译的内容
        try:
            # res = requests.post(self.url,headers=self.headers,proxies={'https':'121.20.97.179:27556'},data=data,timeout=3)  # 获取返回的结果
            res = requests.post(self.url,headers=self.headers,data=data,timeout=3)  # 获取返回的结果
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
        text = '我公司所制造的PXJ 800×400、800800800×600、800×800、1000×1000第三代制砂机(高效细碎机)，是参考各型破碎机的工作原理，并根据用户具体使用情况的信息反馈，结合其优点所设计的新型河卵石制砂机（第三代制砂机）。其典型用途在于适应当前人工机制砂行业，是棒磨式制砂机、冲击式制砂机、直通式制砂机的替代产品。'
        text = '锤式破碎机（简称锤破）是最常用的一种破碎设备，破碎比大（一般为10%-25%，高者达<=50），生产能力高，产品均匀，过粉现象少，单位产品能耗低，结构简单，设备质量轻，操作维护容易等。'
        text = '制砂机设备特点与技术优势：1、处理量大，产量高 125mm～1020mm 50-500t/h，与同等功率下的传统设备相比，产量提高了30%而且稳定。2、易损件消耗低 － 最佳的破碎腔物料撞击角度设计，与耐磨件的摩擦少，比传统设备运行费用低40%，直接降低了设备的使用成本。3、产品粒型优异 － 产品呈立方体，粒型好、级配合理、细度模数可调整的特别适合人工制砂和石料整形，实践证明比其它传统设备制砂、整形效果提高30%。4、液压装置，易于维护 － 液压开盖装置，使破碎内部件检修拆换方便快捷，缩短了停机时间，省时省力。5、稀油润滑，自动保养 － 采用原装进口的稀油润滑站，双油泵互补保证供油；无油流、无油压时自动停机；水冷降温，冬季电机加热启动。6、安装简便，易于操作 － 设备重量轻、安装方式多样，可移动式安装；安装、维修和保养简单，操作使用方便；一旦明确具体的用途，制砂机只需进行细微调整，便可最大限度地发挥其卓越的性能。7、一机多用，运用灵活 － 独有的进料破碎结构，拥有多种破碎腔型，可很方便的实现“石打石”和“石打铁”的转换，从而解决了一机多用 的难题。如果需要改变VSI制砂机的应用 ，无需做大的调整，既可适应用户的不同需求：制砂、整型、磨蚀物料等。8、国际品质保证 － 国外最新技术工艺先进的铆接技术应用以及汽车工艺的外观喷砂除夕处理和喷漆工艺应用，极大的提高了设备的内在质量和外观品质。核心零部件均选用国际著名品牌（轴承采用高精度等级的滚动轴承），确保系统低故障率。9、注重环保 － 设备工作噪音小、无污染。独特的空气自循环系统，大大降低了外排风量，降低粉尘，利于环保。此外VSI破碎机预留并适合安装多种规格的除尘设备。'
        print(text)
        text=google.googleTranslate2(text)
        print(text)
