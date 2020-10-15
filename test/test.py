import selenium
import time
import hashlib
from selenium import webdriver
import os
import pymysql
import re
import xlwt
import xlrd
import xlutils
from selenium.webdriver.chrome.options import Options
url="获得 31 条结果，以下是第 4 页"
print(url)
res=re.findall(r'\d+', url)
print(res)
def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿

# file = xlwt.Workbook(encoding = 'utf-8')
# table = file.add_sheet('data')
# table.write(0,0,url)
# file.save(r'C:\Users\CYG\Desktop\data.xlsx')
write_excel_xls_append(r'C:\Users\CYG\Desktop\data.xlsx',"获得 31 条结果，以下是第 4 页")