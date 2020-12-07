# 对网上手动提取的 html 代码进行处理
# 并不直接从 icdm 官网上爬取

from pyquery import PyQuery

from GoogleTranslate import GoogleTranslate

with open('1.txt', 'r', encoding = 'utf-8') as f:
    html = ''.join(f.readlines())
table_pyquery = PyQuery(html)
paper_list = table_pyquery.find('tr')[1:]
with open('result.txt', 'a', encoding = 'utf-8') as f:
    for paper in paper_list:
        paper_content = list(PyQuery(paper)('td'))
        title = PyQuery(paper_content[1]).text()
        print(title, file = f)
        print(GoogleTranslate.translate('en', 'zh-CN', title), file = f)
        author = PyQuery(paper_content[2]).text()
        print(author, file = f)
        highlight = PyQuery(paper_content[3]).text()
        print(GoogleTranslate.translate('en', 'zh-CN', highlight), file = f)
        print(file = f)
        f.flush()
