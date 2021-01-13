from urllib import request,parse
import json

def translate(content):
    url = "http://fanyi.baidu.com/sug"
    headers = {
        'User-Agent':'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10'
    }
    data = parse.urlencode({"kw":content})  # 将参数进行转码
    req = request.Request(url,data=bytes(data,encoding="utf-8"),headers=headers)
    r = request.urlopen(req)
    # print(r.code) 查看返回的状态码
    html = r.read().decode('utf-8')
    # json格式化
    html = json.loads(html)
    print(html)
    for k in html["data"]:
        print(k["k"],k["v"])

if __name__ == '__main__':
    content = input("请输入您要翻译的内容：")
    translate(content)