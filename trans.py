import sys
from GoogleTranslate import translate


def connection(content):
    content = ''.join(content.split('\n'))
    content = ''.join(content.split('\x02'))
    content = content.replace('. ', '.\n')
    content = content.replace('  ', ' ')
    content = content.replace('\n ', '\n')
    content = content + '\n'
    return content


if __name__ == '__main__':
    file_name = sys.argv[1]
    with open(file_name, 'r', encoding = 'gbk', errors = 'ignore') as f:
        content = ' '.join(f.readlines())
    content = connection(content)
    content = translate('en', 'zh-CN', content)
    print(content)
    with open(file_name, 'w', encoding = 'utf-8') as f:
        print(content, file = f)
