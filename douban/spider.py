# _*_ coding: utf-8 _*_
"""爬取拉钩"""
import requests
from pymongo import MongoClient
import time
from fake_useragent import UserAgent

client = MongoClient()
db = client.lagou2
lagou = db.lagou

headers = {
            'Cookie': 'user_trace_token=20170821145915-a9107b9e-9ee8-41e0-a173-590a40040ccb; LGUID=20170821145916-3f76a9e9-863e-11e7-8dfa-5254005c3644; JSESSIONID=ABAAABAABEEAAJA3063531735537BB84A43E6DEF2D2C2E2; _putrc=91403EB1336FB7B1; login=true; unick=%E5%88%98%E5%AE%89%E6%A3%AE; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=10; TG-TRACK-CODE=search_code; LGSID=20171122091027-ecf527a8-cf21-11e7-9cc2-525400f775ce; LGRID=20171122095800-91cbcbed-cf28-11e7-9ccc-525400f775ce; _gid=GA1.2.2052146106.1511256105; _gat=1; _ga=GA1.2.538073542.1503298803; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1510623133,1510970313,1511159455,1511256107; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1511315940; SEARCH_ID=c1aac000958140cd8bbdcac829371f45; index_location_city=%E6%B7%B1%E5%9C%B3',
            'Referer': 'https://www.lagou.com/jobs/list_iOS?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }


def get_job_info(page, kd):
    for i in range(page):
        url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&city=%E5%8E%A6%E9%97%A8&needAddti' \
              'onalResult=false&isSchoolJob=0'
        payload = {
            'first': 'true',
            'pn': str(i),
            'kd': kd,
        }

        ua = UserAgent()
        headers['User-Agent'] = ua.random

        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            job_json = (response.json()['content']['positionResult']['result'])
            lagou.insert(job_json)
        else:
            print("Something Wrong")

        print("正在爬取" + str(i+1) + "页")
        time.sleep(3)


if __name__ == '__main__':
    get_job_info(24, 'ios')

