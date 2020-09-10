#!/usr/bin/python
# -*- encoding:utf-8 -*-
import json
import requests
from urllib.parse import quote

from GoogleTranslate.cookies import headers


def _get_translate_url(from_language, to_language, translate_text):
    key = quote(translate_text, encoding = 'gbk')
    query_dict = {
        'client': 'at',
        'sl':     from_language,
        'tl':     to_language,
        'dt':     't',
        'q':      key
    }
    url = 'https://translate.google.cn/translate_a/single?'
    for k, v in query_dict.items():
        url = url + k + '=' + v + '&'
    print(url)
    return url


def _get(url):
    try:
        res = requests.get(url, verify = True, headers = headers, timeout = 3)
    except requests.exceptions.MissingSchema:
        return '', 404
    return res.text, res.status_code


def getTranslateResult(translateJson):
    result = ""
    try:
        translateJson = translateJson[0]
        for text in translateJson:
            result = result + text[0]
    except TypeError:
        result = ""
    return result


def translate(from_language, to_language, word):
    url = _get_translate_url(from_language, to_language, word)
    translateRes, code = _get(url)
    if code is not 200:
        print('status code is ', code)
        return ''
    jsonArray = json.loads(translateRes.lower())
    return getTranslateResult(jsonArray)
