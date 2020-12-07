#!/usr/bin/python
# -*- encoding:utf-8 -*-
import requests
from urllib.parse import quote

import TkParams
import json

cookies = [
    '_ga=GA1.3.1058806942.1531796090; NID=182=k5XIOE2zGfcgE2KEP4iTQWpzGcWXQpEHZhBh_3BF9lRwlnxyn24W2jnTaXfadXinVn6ZVa4Mkpk8HZS02sF7adR-6XI60kfQMEut5c9VQgZxDfgJnatiVzhS7qrHyZ4zP3bamIWHZ16BxtOPfiLeAsgxbUu9g_0XzqSAqgQp9GI; _gid=GA1.3.1828501068.1558528281; 1P_JAR=2019-5-23-0; _gat=1',
    '_ga=GA1.3.1058806942.1531796090; _gid=GA1.3.366383484.1556091451; NID=182=k5XIOE2zGfcgE2KEP4iTQWpzGcWXQpEHZhBh_3BF9lRwlnxyn24W2jnTaXfadXinVn6ZVa4Mkpk8HZS02sF7adR-6XI60kfQMEut5c9VQgZxDfgJnatiVzhS7qrHyZ4zP3bamIWHZ16BxtOPfiLeAsgxbUu9g_0XzqSAqgQp9GI; 1P_JAR=2019-4-25-0; _gat=1'
]


class constant:
    cookie_index = 0


""" get translate url """


def _get_translate_url(from_language, to_language, translate_text):
    TkParams.refresh_tkk()
    tk = TkParams.acquire(translate_text)
    print(translate_text)
    key = quote(translate_text)
    print(key)
    sl = from_language
    tl = to_language
    url = 'https://translate.google.cn/translate_a/single?client=webapp&sl=%s&tl=%s&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&otf=1&pc=1&ssel=0&tsel=0&kc=3&tk=%s&q=%s' % (sl, tl, tk, key)
    print(url)
    return url


def _get(url):
    cookie_len = len(cookies)
    constant.cookie_index += 1
    constant.cookie_index %= cookie_len
    headers = {'content-type': 'application/json; charset=UTF-8',
               'accept-language': 'zh-CN,zh;q=0.9',
               "content-disposition": "attachment; filename=\"f.txt\"",
               'Accept-Encoding': '',
               "cookie": cookies[constant.cookie_index],
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
               "accept": "text/html",
               "x-client-data": "CJe2yQEIo7bJAQjEtskBCKmdygEIqKPKAQixp8oBCOKoygEI8anKAQivrMoBGIKYygE=",
               "accept-Charset": "UTF-8"}
    try:
        res = requests.get(url, verify=True, headers=headers, timeout=3)
    except:
        return '', 404
    return res.text.encode('UTF-8').decode('UTF-8'), res.status_code


""" 获取结果列表的第一个翻译 """


def getTranslateResult(translateJson):
    result = ""
    translateJson = translateJson[0] if translateJson is not None else None
    translateJson = translateJson[:-1] if translateJson is not None else None
    if translateJson is not None:
        for text in translateJson:
            result = result + text[0]
    return result


def translate(from_language, to_language, word):
    url = _get_translate_url(from_language, to_language, word)
    translateRes, code = _get(url)
    if code is not 200:
        return ''
    jsonArray = json.loads(translateRes.lower())
    return getTranslateResult(jsonArray)


if __name__ == '__main__':
    print(translate('zh-CN', 'en', '你好'))
