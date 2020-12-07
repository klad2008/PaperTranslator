import math
import re
import requests


class constant:
    TKK = '432247.1200919766'  # this value maybe change by google ,then we need update


def rshift(val, n):
    """python port for '>>>'(right shift with padding) """
    return (val % 0x100000000) >> n


def _xr(a, b):
    size_b = len(b)
    c = 0
    while c < size_b - 2:
        d = b[c + 2]
        d = ord(d[0]) - 87 if 'a' <= d else int(d)
        d = rshift(a, d) if '+' == b[c + 1] else a << d
        a = a + d & 4294967295 if '+' == b[c] else a ^ d

        c += 3
    return a


def acquire(text):
    a = []
    # Convert text to ints
    for i in text:
        val = ord(i)
        if val < 0x10000:
            a += [val]
        else:
            # Python doesn't natively use Unicode surrogates, so account for those
            a += [
                math.floor((val - 0x10000) / 0x400 + 0xD800),
                math.floor((val - 0x10000) % 0x400 + 0xDC00)
            ]

    b = constant.TKK
    d = b.split('.')
    b = int(d[0]) if len(d) > 1 else 0

    # assume e means char code array
    e = []
    g = 0
    size = len(text)
    while g < size:
        l = a[g]
        # just append if l is less than 128(ascii: DEL)
        if l < 128:
            e.append(l)
        # append calculated value if l is less than 2048
        else:
            if l < 2048:
                e.append(l >> 6 | 192)
            else:
                # append calculated value if l matches special condition
                if (l & 64512) == 55296 and g + 1 < size and \
                        a[g + 1] & 64512 == 56320:
                    g += 1
                    l = 65536 + ((l & 1023) << 10) + (a[g] & 1023)  # This bracket is important
                    e.append(l >> 18 | 240)
                    e.append(l >> 12 & 63 | 128)
                else:
                    e.append(l >> 12 | 224)
                e.append(l >> 6 & 63 | 128)
            e.append(l & 63 | 128)
        g += 1
    a = b
    for i, value in enumerate(e):
        a += value
        a = _xr(a, '+-a^+6')
    a = _xr(a, '+-3^+b+-f')
    a ^= int(d[1]) if len(d) > 1 else 0
    if a < 0:  # pragma: nocover
        a = (a & 2147483647) + 2147483648
    a %= 1000000  # int(1E6)

    return '{}.{}'.format(a, a ^ b)


def _get(url):
    headers = {'content-type': 'application/json; charset=UTF-8',
               'accept-language': 'zh-CN,zh;q=0.9',
               "content-disposition": "attachment; filename=\"f.txt\"",
               'Accept-Encoding': '',
               "cookie": "_ga=GA1.3.1058806942.1531796090; _gid=GA1.3.743573119.1555898451; 1P_JAR=2019-4-22-2; NID=181=B4bCvuoYOtOPbrQB1626zFADiTQkwCg7F8AYSi1heEAi08NXZGTrYLqDyqjvmX3O_wzaVDq2SBk9gIQE2aKFiGOQqCW6PEcsHyH9gvEqnXa81gq0fhjsq_5UNXY2JWTdRdQB_Da9sAHLG-S5vcDx0SxMvx9qcX--hJmWcYzVLeU",
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
               "accept": "text/html",
               "accept-Charset": "UTF-8"}
    try:
        res = requests.get(url, verify=True, headers=headers, timeout=3)
    except:
        return '', 404
    return res.text.encode('UTF-8').decode('UTF-8'), res.status_code


# refresh tkk key
def refresh_tkk():
    text, code = _get("https://translate.google.cn/")
    if code != 200:
        return False
    text = re.findall(r'tkk(.+?),', text)
    constant.TKK = re.sub(':|\'', '', text[0])
    return True
