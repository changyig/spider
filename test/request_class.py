import requests
from lxml import etree
import json
import re
class myrequest:
    def __init__(self):
        self.records_num = 0
        self.records_text = ''
        self.site = ''
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
        self.cookies = self.read_txt_cookie()
    '''
    读取txt 配置cookie信息
    '''
    def read_txt_cookie(self):
        data_dict = {}
        with open('./txt/cookie.txt','r') as f:
            data = f.read().split(';')
            for i in data:
                cookie_item = i.split('=')
                data_dict[cookie_item[0].strip()] = cookie_item[1].strip()
        return data_dict
    '''
    说明:通过get方式获取网站信息 并以json格式将获取到的数据返回出去
    '''
    def query_msg(self):
        url = 'https://baidurank.aizhan.com/baidu/163.com/'
        html = requests.get(url,headers=self.headers,cookies=self.cookies)
        filename = r'C:\Users\CYG\Desktop\test.html'
        data_dict=[]
        if html.status_code == 200:
            with open(filename,'wb') as f:
                f.write(html.content)
            res=etree.HTML(html.content).xpath("//td[@class='title']")
            for index, td in enumerate(res):
                if index !=0:
                    # print(td.xpath('string(.)'))
                    data_dict.append(''.join(td.xpath('string(.)').split()))
        # print(json.dumps(data_dict))
        return json.dumps(data_dict)


    '''
    说明:过滤掉多个空格只保留一个空格
    '''
    def stain_space(self,text=''):
        pattern = re.compile("\r\n")
        text = pattern.sub('',text)
        text = ' '.join(text.split())
        return text

    '''
       说明:组合参数 get方式参数
       '''
    def combine_get_params(self,dicts):
        string = ''
        for dict in dicts.items():
            if string == '':
                string += str(dict[0]) + '=' + str(dict[1])
            else:
                string += '&' + str(dict[0]) + '=' + str(dict[1])
        string = '?' + string
        print(string)
        return string
    def get_domain_message(self,web_id,domain_name):
        url = 'http://172.16.10.90:88/!admin/List-WebDetails.aspx'
        dict = {'WebId':web_id,'webname':domain_name}
        url = url + self.combine_get_params(dict)
        print(url)
        html = requests.get(url,headers=self.headers,cookies=self.cookies)
        print(html)
        if html.status_code == 200:
            try:
                ip = etree.HTML(html.content).xpath("//input[@id='ctl00_main_TextBox_WIP']/@value")[0]
                name = etree.HTML(html.content).xpath("//input[@id='ctl00_main_TextBox_WFTPUser']/@value")[0]
                pwd = etree.HTML(html.content).xpath("//input[@id='ctl00_main_TextBox_WFTPPwd']/@value")[0]
                database = etree.HTML(html.content).xpath("//textarea[@id='ctl00_main_TextBox_WFTPConn']")[0].xpath(
                    'string(.)')
                database = self.stain_space(database)
                print(ip,name,pwd,database)
                return ip,name,pwd,database
            except Exception as e:
                print(e)
                print('域名ftp信息尚未填写，确认后在尝试获取')
                return False
            # ip_text = ip.xpath('string(.)')
            # print(ip_text)

    def filter_txt(self,text=''):
        pattern = re.compile("[^0-9^a-zA-Z^.^|^-]")
        text = pattern.sub('',text)
        return text
    '''
        说明：通过黑色后台url链接地址 获取最近分配的域名 并把它存入指定的excel文件中

    '''
    def get_message(self):
        url = 'http://172.16.10.90:88/!admin/List-WebStatus.aspx'

        dict = {'kfuserid':626,'IndustryID':0,'SclassID':0,'Show':'','Wtags':'','Host':'','zuhe':0,'order':'desc'}
        url = url + self.combine_get_params(dict)

        html = requests.get(url,headers=self.headers,cookies=self.cookies)
        filename = r'C:\Users\CYG\Desktop\test.html'
        if html.status_code == 200:
            with open(filename,'wb') as f:
                f.write(html.content)
            dicts = {'domain_name' :'','web_id':'','ip':'','ftp_name':'','ftp_pwd':'','database_name':'',
                     'database_pwd':''}
            td_id = etree.HTML(html.content).xpath("//table[@id='ctl00_main_GridView1']//tr[2]//td[1]")[0]
            # td_id_text = etree.tostring(td_id,method='html')
            td_id_text = td_id.xpath('string(.)')
            td_domain = etree.HTML(html.content).xpath("//table[@id='ctl00_main_GridView1']//tr[2]//td[7]")[0]
            td_domain_text = td_domain.xpath('string(.)')
            td_id_text = self.filter_txt(td_id_text)
            td_domain_text = self.filter_txt(td_domain_text)
            web_id = td_id_text.split('|')[1]
            domain_name = td_domain_text.split('|')[0]
            print(web_id,domain_name)
            res = self.get_domain_message(web_id,domain_name)
            if res:
                dicts['domain_name'],dicts['web_id'],dicts['ip'],dicts['ftp_name'],dicts['ftp_pwd'],dicts[
                    'database_name'],dicts['database_pwd'] =\
                    domain_name,web_id,res[0],res[1],res[2],res[3].split(' ')[0],res[3].split(' ')[1]
                print(dicts)
                path = r'E:\红星办公文件\xls表格文档\域名分配\域名分配.xlsx'
                write_exce(path,dicts)