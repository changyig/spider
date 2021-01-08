from bs4 import BeautifulSoup
import requests
# from urllib3 import request
import urllib3
import os

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
def test(url):
    path1 = url.split('/')[-1]
    str_list=path1.replace('.html','').split('-')
    str=' '.join(str_list)
    write_keyword(str)
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
def test_url():
    url='https://www.ftmmachinery.com/blog/stone-crusher-plant-price-for-sale.html'
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    print(r)
    print(soup)
    print(soup.title.string)
# test_url()
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

write_sitemap()