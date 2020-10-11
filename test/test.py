import selenium
import time
import hashlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# chrome_options = Options()
options = webdriver.ChromeOptions()
path="D:\\soft\\anaconda\\chromedriver.exe"
options.add_argument("user-data-dir=D:\data\scrapy" )
options.binary_location = r"C:\Users\CYG\AppData\Local\Google\Chrome\Application\chrome.exe"
def proxy():
    #https://www.hailiangip.com/tool/page/code 代理商使用的地址
    orderId = "O20101117292659712964"
    secret = "58faf5fb12c9424a81d3d5c8fd3574dd"
    host = "flow.ipproxy.info"
    port = "14223"
    user = "proxy"
    timestamp = str(int(time.time()))  # 计算时间戳
    txt = "orderId=" + orderId + "&" + "secret=" + secret + "&" + "time=" + timestamp
    txt = txt.encode()
    sign = hashlib.md5(txt).hexdigest()  # 计算sign
    password = 'orderId=' + orderId + '&time=' + timestamp + '&sign=' + sign + "&pid=-1" + "&cid=-1" + "&uid=" + "&sip=0" + "&nd=0"
    # print(password)
    proxyUrl = "--proxy-server=http://" + user + ":" + password + "@" + host + ":" + port
    # print(proxyUrl)
    return proxyUrl
# proxy_url=proxy()
# options.add_argument(proxy_url)
# options.add_argument("--proxy-server=http://123.156.181.176:4281")

# options.add_argument("--headless" )
browser=webdriver.Chrome(options=options,executable_path=path)

def write_txt(keyword,filename):
    make_file(filename)
    with open(filename, "a", encoding='utf-8') as f:
        f.write(keyword+'\n')
def get_infos_url(url):
    browser.get(url)
    lists_infos = browser.find_elements_by_class_name('js-fanyi-result')
    for list in lists_infos:
        # print(list)
        try:
            keyword=list.find_element_by_tag_name('h3').text
            info=list.find_element_by_class_name('ft').text
            print('title内容为：'+keyword)
            print('详情内容：'+info)
            sleep(1)
        except:
            print('出现错误')

if __name__=="__main__":
    # proxy()
    page = 4
    url = "https://english.sogou.com/english?query={}&fr=common_nav&b_o_e=1&page={}&ie=utf8&pagenumtype=global"
    with open(r"./test.txt", 'r', encoding='utf-8') as infile:
        for line in infile:
            str = line.rstrip('\n')
            keyword=str.replace(' ','+')
            print('当前关键词:{}'.format(keyword))
            for i in range(1,page):
                page_url=url.format(keyword,i)
                print('第{}页获取到的内容,当前链接地址：{}'.format(i, page_url))
                get_infos_url(page_url)

    #


