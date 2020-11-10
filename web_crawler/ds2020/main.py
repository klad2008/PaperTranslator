import json

import numpy
import pandas
import requests

from web_crawler.ds2020.user_id import user_id

oj_ip = "http://10.192.11.200"
root_id = "root"
root_pw = "fudan-0j!"
contest_id = 17
problems_total = 3
problems_start = 2005
contest_problems_list = [chr(x) for x in range(ord('A'), ord('A') + problems_total)]
repair_problems_list = [str(x + problems_start) for x in range(problems_total)]
full_problems_list = contest_problems_list + repair_problems_list
print(full_problems_list)

r_host = requests.get(oj_ip + "/api/profile")
cookies = r_host.cookies.get_dict()
headers = {
    "Accept":          "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection":      "keep-alive",
    "Content-Length":  "42",
    "Content-Type":    "application/json;charset=UTF-8",
    "Cookie":          "csrftoken=" + cookies['csrftoken'],
    "User-Agent":      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/76.0.3809.132 Safari/537.36",
    "X-CSRFToken":     cookies['csrftoken']
}
data = {"username": root_id, "password": root_pw}
r_login = requests.post(oj_ip + "/api/login", data = json.dumps(data), headers = headers)
print(r_login.text)
cookies = r_login.cookies.get_dict()
headers = {
    "cookie": "sessionid=" + cookies['sessionid']
}


contest_result = numpy.zeros((len(user_id), len(full_problems_list)))
contest_result = pandas.DataFrame(contest_result, columns = full_problems_list, index = user_id)

page = 0
while True:
    r_info = requests.get(
        oj_ip + "/api/contest_submissions?result={}&page={}&contest_id={}&limit={}&offset={}".format(
            0, page+1, contest_id, 12, 12 * page
        ),
        headers = headers)
    infolist = json.loads(r_info.text)['data']
    infolist = infolist['results']
    if len(infolist) == 0:
        break
    page += 1
    for info in infolist:
        problem_id = info['problem']
        username = info['username']
        contest_result.at[username, problem_id] = 1


for username in user_id:
    for idx in range(problems_total):
        if contest_result.at[username, contest_problems_list[idx]] == 1:
            continue
        problem_id = repair_problems_list[idx]
        r_info = requests.get(
            oj_ip + "/api/submissions?result={}&username={}&page={}&problem_id={}&limit={}&offset={}".format(
                0, username, page + 1, problem_id, 12, 0
            ),
            headers = headers)
        infolist = json.loads(r_info.text)['data']
        infolist = infolist['results']
        if len(infolist) == 0:
            break
        contest_result.at[username, repair_problems_list[idx]] = 1


contest_result.sort_index(axis = 0)
csv_name = 'contest_{}.csv'.format(contest_id)
contest_result.to_csv(csv_name)

