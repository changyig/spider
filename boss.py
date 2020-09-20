# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup


def get_one_page_info(kw, page):
    '''获取第page的数据，搜索关键字kw'''
    url = "https://www.zhipin.com/c101020100/?query=" + kw + "&page=" + str(page) + "&ka=page-" + str(page)
    cookies = {
        "lastCity": "101180100",
        "_uab_collina": "156594127160811552815566",
        "sid": "sem_pz_bdpc_dasou_title",
        "__c": "1578311883",
        "__g": "-",
        "__l": "l=%2Fwww.zhipin.com%2Fchongqing%2F&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DyAJ9Ih3bUYCO1UZEdz7NJjsnd64hlHOGAUnPQOvlf2yarY3ANI95kfOTH6lIzZ4H%26wd%3D%26eqid%3Ddc757f2800099ca2000000065e1320c3&friend_source=0&friend_source=0",
        "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a": "1578311884",
        "Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a":"1578314390",
        "__zp_stoken__": "e768REDN6Uxi7wTuQpfZn6BqGEppb59VUfZ4uUGJl6yMcoUPA6dpKLq3v6pZuR8%2BNm%2BclR%2Fe2aXv1%2FRr%2B07rA8PWDaJPzZ2aqDTGcx4ILvF%2BuUP8iNrAyyrc%2F1TiKYKVq%2F0L",
        "__a": "53332382.1578311883..1578311883.8.1.8.8",
    }
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "referer": "https://www.zhipin.com/c101020100/?query=python%E5%BC%80%E5%8F%91&page=1&ka=page-1"
    }
    r = requests.get(url, headers=headers, cookies=cookies)
    # soup = BeautifulSoup(r.text, "lxml")
    with open("test2.html","w",encoding='utf-8') as f:
        f.write(r.text)
    # print(soup)




for i in range(1, 2):
    infos = get_one_page_info("python开发", i)
    # save_mysql(infos)