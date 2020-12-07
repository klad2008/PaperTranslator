with open('title.txt', 'r', encoding = 'utf-8') as f:
    s = f.readlines()

for i in range(0, len(s), 3):
    print(s[i])

# https://nips.cc/Conferences/2020/AcceptedPapersInitial
# 直接翻译 accepted-paper 的标题，手工调整因特殊字符而换行的标题。
