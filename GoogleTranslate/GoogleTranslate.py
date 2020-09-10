#!/usr/bin/python
# -*- encoding:utf-8 -*-
import json
import requests
from urllib.parse import quote, unquote

from GoogleTranslate import TkParams
from GoogleTranslate.cookies import headers


def _get_translate_url(from_language, to_language, translate_text):
    TkParams.refresh_tkk()
    tk = TkParams.acquire(translate_text)
    key = quote(translate_text)
    query_list = (
        ('client', 'webapp'),
        ('sl', from_language),
        ('tl', to_language),
        ('hl', 'zh-CN'),
        ('dt', 't'),
        ('otf', '1'),
        ('pc', '1'),
        ('ssel', '0'),
        ('tsel', '0'),
        ('kc', '3'),
        ('tk', tk),
        ('q', key)
    )
    url = 'https://translate.google.cn/translate_a/single?'
    for k, v in query_list:
        url = url + k + '=' + v + '&'
    return url


def _get(url):
    try:
        res = requests.get(url, verify = True, headers = headers, timeout = 3)
    except requests.exceptions.MissingSchema:
        return '', 404
    return res.text.encode('UTF-8').decode('UTF-8'), res.status_code


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
