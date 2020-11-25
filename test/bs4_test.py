from bs4 import BeautifulSoup
import requests


# r = requests.get(url, headers=headers, cookies=cookies)
# soup = BeautifulSoup(content,"html.parser")
def write_keyword(keyword):
    with open("./keyword.txt", "a", encoding='utf-8') as f:
        f.write(keyword + '\n')

def read_xml():
    print(2)
    # url = 'https://www.fruitfuler.com/sitemap.xml'
    # url = 'https://www.urbanjournalism.de/sitemap.xml'
    url = 'https://www.bouwwerken-dekleermaeker-liekens.be/sitemap.xml'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "xml")
    # print(soup)
    count = soup.find_all(name="loc")
    num = 0
    for i in count:
        url_text = i.string
        res = requests.get(url_text)
        soup2 = BeautifulSoup(res.text, "xml")
        keyword_url = soup2.find_all(name="loc")
        for word in keyword_url:
            keyword = word.string
            if keyword.find('.html') > 0:
                print(keyword)
                test(keyword)

def test(url):
    path1 = url.split('/')[-1]
    str_list = path1.replace('.html', '').split('-')
    str = ' '.join(str_list)
    write_keyword(str)
def get_keyword_url():
    # url = 'https://english.sogou.com/english?query=jaw+crusher&fr=common_nav&b_o_e=1&page=4&ie=utf8&pagenumtype=global'
    url = 'https://mijisou.com/?q=crusher+machine&category_general=on&time_range=&language=zh-CN&pageno=3'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    # title = soup.title.text
    # h1 = soup.h1.text
    # description = soup.find('h1').find_next_sibling()
    print(soup)
    # print(h1)
    # print(description)
get_keyword_url()
