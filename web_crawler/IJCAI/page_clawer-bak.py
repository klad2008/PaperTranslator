# 连接 ijcai 官网
# 没有工具连不上网站
# 此外还需要debug
import json

from pyquery import PyQuery
import requests
from GoogleTranslate import GoogleTranslate


class page_clawer:
    def __init__(self):
        pass
    
    def translate_en2cn(self, text):
        text_ = GoogleTranslate.translate('en', 'zh-CN', text)
        return text_
    
    def save_log(self, log_dic):
        with open('page_clawer.log', 'w', encoding = 'utf-8') as f:
            print(json.dumps(log_dic), file = f)
    
    def load_log(self):
        with open('page_clawer.log', 'r', encoding = 'utf-8') as f:
            log_dic = json.load(f)
        return log_dic
    
    def connect(self, url):
        try:
            print('connecting : ', url, ' ......')
            req = requests.get(url)
        except Exception as e:
            print('\n-----------------')
            print(e)
            print('-----------------\n')
            req = self.connect(url)
        return req
    
    def paper_page(self, url):
        req = self.connect(url)
        page_pyquery = PyQuery(req.text)
        post_pyquery = page_pyquery('.container-fluid.proceedings-detail')
        output = []
        paper_header = PyQuery(post_pyquery('.row')[0])
        paper_header = paper_header.children()[0]
        title = paper_header('h1').text()
        output.append(title + '\n')
        author = paper_header('h2').text()
        output.append('\t' + author + '\n')
        contain = PyQuery(post_pyquery('.row')[2])
        abstract = contain.children()[0].text()
        abstract = self.translate_en2cn(abstract)
        output.append('\t' + abstract + '\n')
        return output
    
    def subsection_process(self, subsection_pyquery, log_dic):
        paper_list = subsection_pyquery('.paper_wrapper')
        for step in range(log_dic['step'], len(paper_list)):
            paper_pyquery = PyQuery(step)
            title = paper_pyquery('.title').text()
            href_pyquery = paper_pyquery('.details').children('[href]')[1]
            href = 'https://www.ijcai.org' + href_pyquery.attr('href')
            output = self.paper_page(href)
            print('finish. step = ', step, '\t; ', title)
            with open('result.txt', 'a', encoding = 'utf-8') as f:
                f.writelines(output)
                f.write('\n')
                f.flush()
            log_dic['step'] = step
            self.save_log(log_dic)
    
    def __call__(self, url):
        log_dic = self.load_log()
        if 'url_log' not in log_dic or log_dic['url_log'] != url:
            print('url is not same as last time')
            log_dic['url_log'] = url
            log_dic['subsection'] = 0
            log_dic['step'] = 0
            with open('result.txt', 'w', encoding = 'utf-8') as f:
                f.truncate()
        
        page_pyquery = PyQuery(self.connect(url).text)
        paperlist_pyquery = list(page_pyquery('.subsection'))
        
        for subsection in range(int(log_dic['subsection']), len(paperlist_pyquery)):
            self.subsection_process(PyQuery(paperlist_pyquery[subsection]), log_dic)
            log_dic['subsection'] = subsection + 1
            log_dic['step'] = 0


if __name__ == '__main__':
    page_clawer()("https://www.ijcai.org/Proceedings/2020/")
