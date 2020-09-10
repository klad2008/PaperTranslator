import requests
from pyquery import PyQuery

from GoogleTranslate.GoogleTranslate import translate


class page_clawer:
    def __init__(self):
        pass
    
    def save_log(self, url, step):
        with open('page_clawer.log', 'w', encoding = 'utf-8') as f:
            print('url: ', url, file = f)
            print('step: ', step, file = f)
    
    def load_log(self):
        with open('page_clawer.log', 'r', encoding = 'utf-8') as f:
            url = f.readline().split('url: ')[1].strip()
            step = int(f.readline().split('step: ')[1])
        return url, step
    
    def connect(self, url):
        try:
            req = requests.get(url)
        except Exception as e:
            print('\n-----------------')
            print(e)
            print('-----------------\n')
            req = self.connect(url)
        return req

    def paper_page(self, url):
        print(url)
        req = self.connect(url)
        container = PyQuery(req.text)('.container')
        output = []
        title = container.children('h2').text()
        output.append(title + '\n')
        author_list = container.children('p').text()
        author_list = author_list.split('; ')
        author_list = ['\t' + x + '\n' for x in author_list]
        output.extend(author_list)
        abstract = container.children('.row').children('.col-lg-9').children('p').text()
        abstract = translate('en', 'zh-CN', abstract)
        output.append('\t' + abstract + '\n')
        return output
    
    def __call__(self, url):
        page_pyquery = PyQuery(requests.get(url).text)
        paperlist_pyquery = list(page_pyquery('.d-block.u-link-v5.g-font-weight-600.g-mb-3'))
        url_log, step_log = self.load_log()
        if url_log != url:
            print('url is not same as last time')
            step_log = 0
            with open('result.txt', 'w', encoding = 'utf-8') as f:
                f.truncate()
        
        with open('result.txt', 'a', encoding = 'utf-8') as f:
            for step in range(step_log, len(paperlist_pyquery)):
                x = paperlist_pyquery[step]
                paper_pyquery = PyQuery(PyQuery(x).children('[href]'))
                href = paper_pyquery.attr('href')
                title = paper_pyquery.text()
                output = self.paper_page(href)
                print('finish. step = ', step, '\t; ', title)
                self.save_log(url, step + 1)
                f.writelines(output)
                f.write('\n')
                f.flush()


if __name__ == '__main__':
    page_clawer()("https://www.kdd.org/kdd2020/accepted-papers")
