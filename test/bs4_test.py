from bs4 import BeautifulSoup
import requests
# r = requests.get(url, headers=headers, cookies=cookies)
# soup = BeautifulSoup(content,"html.parser")
def write_keyword(keyword):
    with open("../test.txt","a",encoding='utf-8') as f:
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
                print(keyword)
                test(keyword)
def test(url):
# def test():
#     url='https://www.fruitfuler.com/114741/instruction/Gravel-Sand-Quarry-Plant-Layout.html'
    path1 = url.split('/')[-1]
    str_list=path1.replace('.html','').split('-')
    str=' '.join(str_list)
    write_keyword(str)
read_url()