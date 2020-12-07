import sys

from pyquery import PyQuery
import requests
import GoogleTranslate


class page_clawer:
    def __init__(self):
        pass
    
    def translate_en2cn(self, text):
        text_ = GoogleTranslate.translate('en', 'zh-CN', text)
        return text_
    
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
        req = self.connect(url)
        page_pyquery = PyQuery(req.text)
        output = []
        title = page_pyquery('.page_title').text()
        output.append(title + '\n')
        author_list = page_pyquery('.authors').children()
        for author in author_list:
            author_pyquery = PyQuery(author)
            author_name = author_pyquery('.name').text()
            author_affiliation = author_pyquery('.affiliation').text()
            output.append('\t' + author_name + '\t' + author_affiliation + '\n')
        abstract = page_pyquery('.abstract').children('p').text()
        abstract = self.translate_en2cn(abstract)
        output.append('\t' + abstract + '\n')
        return output

    def __call__(self, url):
        page_pyquery = PyQuery(requests.get(url).text)
        paperlist_pyquery = list(page_pyquery('#box6').find('.content').find('p.left'))
        url_log, step_log = self.load_log()
        if url_log != url:
            print('url is not same as last time')
            step_log = 0
            with open('result.txt', 'w', encoding = 'utf-8') as f:
                f.truncate()
        
        with open('result.txt', 'a', encoding = 'utf-8') as f:
            for step in range(step_log, len(paperlist_pyquery)):
                x = paperlist_pyquery[step]
                paper_pyquery = PyQuery(PyQuery(x).children('[href]')[0])
                href = paper_pyquery.attr('href')
                title = paper_pyquery.text()
                output = self.paper_page(href)
                print('finish. step = ', step, '\t; ', title)
                self.save_log(url, step + 1)
                f.writelines(output)
                f.write('\n')
                f.flush()


if __name__ == '__main__':
    page_clawer()("https://aaai.org/Library/AAAI/aaai20contents-issue05.php")
