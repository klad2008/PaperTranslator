# 从其他网站爬取标题，无摘要
import json
from pyquery import PyQuery
import requests
from GoogleTranslate import GoogleTranslate


class title_clawer:
    def __init__(self):
        pass
    
    def translate_en2cn(self, text):
        text_ = GoogleTranslate.translate('en', 'zh-CN', text)
        return text_
    
    def connect(self, url, link_info = True):
        try:
            if link_info:
                print('connecting : ', url, ' ......')
            req = requests.get(url)
            if link_info:
                print('connecting success!')
        except Exception as e:
            print('\n-----------------')
            print(e)
            print('-----------------\n')
            req = self.connect(url, link_info = True)
        return req
    
    def __call__(self, url):
        page_pyquery = PyQuery(self.connect(url).text)
        session_list_pyquery = list(page_pyquery('.session'))
        with open('result.txt', 'w', encoding = 'utf-8') as f:
            for session in session_list_pyquery:
                session_name = PyQuery(session).find('h3').text()
                print(session_name, file = f)
                paper_list = list(PyQuery(session).find('.paper'))
                for paper in paper_list:
                    paper_pyquery = PyQuery(paper)
                    title = paper_pyquery.find('strong').text()
                    print(title, file = f)
                    title = self.translate_en2cn(title)
                    print(title, file = f)
                    print(file = f)
                    f.flush()
                print(file = f)
                f.flush()


if __name__ == '__main__':
    title_clawer()("http://static.ijcai.org/2020-accepted_papers.html")
