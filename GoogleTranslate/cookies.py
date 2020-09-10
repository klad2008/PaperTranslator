# Temporarily delete

cookies = [
    '_ga=GA1.3.1058806942.1531796090; NID=182=k5XIOE2zGfcgE2KEP4iTQWpzGcWXQpEHZhBh_3BF9lRwlnxyn24W2jnTaXfadXinVn6ZVa4Mkpk8HZS02sF7adR-6XI60kfQMEut5c9VQgZxDfgJnatiVzhS7qrHyZ4zP3bamIWHZ16BxtOPfiLeAsgxbUu9g_0XzqSAqgQp9GI; _gid=GA1.3.1828501068.1558528281; 1P_JAR=2019-5-23-0; _gat=1',
    '_ga=GA1.3.1058806942.1531796090; _gid=GA1.3.366383484.1556091451; NID=182=k5XIOE2zGfcgE2KEP4iTQWpzGcWXQpEHZhBh_3BF9lRwlnxyn24W2jnTaXfadXinVn6ZVa4Mkpk8HZS02sF7adR-6XI60kfQMEut5c9VQgZxDfgJnatiVzhS7qrHyZ4zP3bamIWHZ16BxtOPfiLeAsgxbUu9g_0XzqSAqgQp9GI; 1P_JAR=2019-4-25-0; _gat=1'
]


class constant:
    cookie_index = 0


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
