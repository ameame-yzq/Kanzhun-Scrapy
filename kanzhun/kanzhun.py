import json
import requests
import execjs
import pandas as pd
import re
from openpyxl import load_workbook
job_name = input('请输入你要搜索的关键字，如python： ')
cookies = {
    'wd_guid': 'b308eb9e-8371-4d6c-a245-969cb31b6ce6',
    'historyState': 'state',
    '__c': '1725696521',
    '__g': '-',
    '__l': 'l=%2Fwww.kanzhun.com%2Fsearch%3FcityCode%3D101010100%26experienceId%3D%26pageNum%3D1%26query%3Dpython%26salaryId%3D%26type%3D5&r=',
    'Hm_lvt_1f6f005d03f3c4d854faec87a0bee48e': '1725524719,1725671801,1725696521',
    'HMACCOUNT': 'BF724002793E3CDE',
    'wbrwsid': '45673881',
    'Hm_lpvt_1f6f005d03f3c4d854faec87a0bee48e': '1725696560',
    '__a': '75909637.1725524722.1725671801.1725696521.27.3.3.27',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    # 'cookie': 'wd_guid=b308eb9e-8371-4d6c-a245-969cb31b6ce6; historyState=state; __c=1725696521; __g=-; __l=l=%2Fwww.kanzhun.com%2Fsearch%3FcityCode%3D101010100%26experienceId%3D%26pageNum%3D1%26query%3Dpython%26salaryId%3D%26type%3D5&r=; Hm_lvt_1f6f005d03f3c4d854faec87a0bee48e=1725524719,1725671801,1725696521; HMACCOUNT=BF724002793E3CDE; wbrwsid=45673881; Hm_lpvt_1f6f005d03f3c4d854faec87a0bee48e=1725696560; __a=75909637.1725524722.1725671801.1725696521.27.3.3.27',
    'href': 'https://www.kanzhun.com/search?cityCode=101010100&experienceId=&pageNum=1&query=python&salaryId=&type=5',
    'priority': 'u=1, i',
    'referer': 'https://www.kanzhun.com/search?cityCode=101010100&experienceId=&pageNum=1&query=python&salaryId=&type=5',
    'reqsource': 'fe',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceid': 'F-87cd23OAhrMZ5a3V',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

page = {
    "query": str(job_name),
    "cityCode": "101020100",
    "salaryId": "",
    "experienceId": "",
    "pageNum": 1,
    "limit": 15
}
str_page = json.dumps(page)
# print(str_page)
page_compile = execjs.compile(open('kanzhun.js').read())
js_compile = page_compile.call('text', str_page)
# print(page_compile)
params = {
    'b': js_compile[1],
    'kiv': js_compile[0],
}
response = requests.get('https://www.kanzhun.com/api_to/search/job.json', params=params, cookies=cookies,
                        headers=headers)
aes_compile = execjs.compile(open('kanzhun.js').read()).call('decrypt', response.text, js_compile[0])

print(aes_compile)
    # 封装正则函数

def extract_data(text):
    pattern_experience = r'"experience":"(.*?)"'
    pattern_degree = r'"degree":"(.*?)"'
    pattern_salary = r'"salary":"(.*?)"'
    pattern_skills = r'"skills":"(.*?)"'

    matches_experience = re.findall(pattern_experience, text)
    matches_degree = re.findall(pattern_degree, text)
    matches_salary = re.findall(pattern_salary, text)
    matches_skills = re.findall(pattern_skills, text)

    return matches_experience, matches_degree, matches_salary, matches_skills


def save_to_excel(extracted_data, output_file):
    # 使用最长的列表作为行数
    max_len = max(len(extracted_data[0]), len(extracted_data[1]), len(extracted_data[2]), len(extracted_data[3]))

    # 填充列表使得长度与最长的列表相同
    data_experience_filled = extracted_data[0] + [''] * (max_len - len(extracted_data[0]))
    data_degree_filled = extracted_data[1] + [''] * (max_len - len(extracted_data[1]))
    data_salary_filled = extracted_data[2] + [''] * (max_len - len(extracted_data[2]))
    data_skills_filled = extracted_data[3] + [''] * (max_len - len(extracted_data[3]))

    # 创建DataFrame
    df = pd.DataFrame({
        'experience': data_experience_filled,
        'degree': data_degree_filled,
        'salary': data_salary_filled,
        'skills': data_skills_filled
    })

    # 存储到Excel文件中
    df.to_excel(output_file, index=False)


if __name__ == "__main__":
    # 读取TXT文件内容
    text = aes_compile

    # 提取数据
    extracted_data = extract_data(text)
    # 存储到Excel
    output_file = f'zhaopin_{job_name}.xlsx'
    save_to_excel(extracted_data, output_file)