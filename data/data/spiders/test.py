import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--headless')
# browser = webdriver.Chrome(options=chrome_options)
page=10
url="https://english.sogou.com/english?query=iran+impact+crusher+for+sale&fr=common_nav&b_o_e=1&page=1&ie=utf8&pagenumtype=global"
url2="https://english.sogou.com/english?query=jaw+crusher&fr=common_nav&pagenumtype=global&b_o_e=1&page=5&ie=utf8&pagenumtype=global"
path="D:\\soft\\anaconda\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=D:\data\scrapy" )
# options.add_argument("--headless" )
# chrome_options.binary_location = r"D:\softs\google\ChromePortable\ChromePortable.exe"
options.binary_location = r"C:\Users\CYG\AppData\Local\Google\Chrome\Application\chrome.exe"
# # # browser = webdriver.Chrome(chrome_options=options)
# # # browser=webdriver.Chrome(chrome_options=options,executable_path=path)
browser=webdriver.Chrome(options=options,executable_path=path)
browser.get(url)
# print(browser.title)
class_name=browser.find_elements_by_class_name('js-fanyi-result')
print(class_name)

# for i in class_name:
#     print(i.text)
page_container=browser.find_element_by_id('pagebar_container')
page_a=page_container.find_elements_by_tag_name('a')
for a_url in page_a:
    print(a_url.get_attribute("href"))
print(page_container)
print(page_a)
print(page_container.text)
# # class_name=browser.find_element_by_id('inp-query').send_keys('我不是药神')
# browser.get(url2)
# class_name2=browser.find_elements_by_class_name('js-fanyi-result')
# print(class_name)
# print(class_name.text)
