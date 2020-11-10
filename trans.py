import re
import sys
from GoogleTranslate import translate


def connection(content):
    content = ''.join(re.split('[\n\x02]', content))
    content = content.replace('. ', '.\n')
    content = content.replace('  ', ' ')
    content = content.replace('\n ', '\n')
    content = content.replace('et al.\n', 'et al.')
    content = content.replace('e.g.\n', 'e.g. ')
    content = content.replace('i.e.\n', 'i.e. ')
    content = content.replace('Eq.\n', 'Eq. ')
    content = content.replace('Fig.\n', 'Fig. ')
    content = content.replace('.\n.\n.\n', '...')
    content = content + '\n'
    return content


if __name__ == '__main__':
    file_name = sys.argv[1]
    with open(file_name, 'r', encoding = 'utf-8', errors = 'ignore') as f:
        content = ' '.join(f.readlines())
    content = connection(content)
    with open(file_name, 'w', encoding = 'utf-8') as f:
        print(content, file = f)
    content = translate('en', 'zh-CN', content)
    with open(file_name, 'w', encoding = 'utf-8') as f:
        print(content, file = f)
