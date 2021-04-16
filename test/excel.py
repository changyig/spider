import selenium
import time
import hashlib
from selenium import webdriver
import os
import pymysql
import re
import xlwt
import xlrd
from xlutils.copy import copy
from selenium.webdriver.chrome.options import Options
def write_excel_xls_append(path, value):
    # index = len(value)  # 获取需要写入数据的行数
    index = 1  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    j=0
    for i in range(0, index):
        new_worksheet.write(i+rows_old, j, value)  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
def write_exce(path,url,nums,remark=''):
    # res = re.findall(r'\d+', content)
    # index = len(value)  # 获取需要写入数据的行数
    index = 1  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    j = 0
    date=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    new_worksheet.write(0 + rows_old, j, url)  # 追加写入数据，注意是从i+rows_old行开始写入
    new_worksheet.write(0 + rows_old, j+1, nums)
    new_worksheet.write(0 + rows_old, j+2, remark)
    new_worksheet.write(0 + rows_old, j+3, date)
    new_workbook.save(path)  # 保存工作簿
    print('当前网站:{},site收录数量:{},收录信息:{},当前日期:{}'.format(url,nums,remark,date))
def txt_excel():
    open_filename=r'C:\Users\CYG\Desktop\res.txt'
    excel_filename=r'C:\Users\CYG\Desktop\data.xlsx'
    with open(open_filename,mode='r',encoding='utf-8') as ff:
        for i in ff.readlines():
            str = i.split('|')
            url=str[0]
            num=str[1]
            print(url,num)
            write_excel(excel_filename,url,num)
txt_excel()
# file = xlwt.Workbook(encoding = 'utf-8')
# table = file.add_sheet('data')
# table.write(0,0,url)
# file.save(r'C:\Users\CYG\Desktop\data.xlsx')
# write_excel_xls_append(r'C:\Users\CYG\Desktop\data.xlsx',"获得 31 条结果，以下是第 4 页")