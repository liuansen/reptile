# _*_ coding: utf-8 _*_
__author__ = 'Anson'
__date__ = '2017/11/21 16:34 '
# 爬取知乎用户粉丝信息
import requests
import pandas as pd
import time


# 加载浏览器头部信息
headers = {
    'authorization': 'Bearer Mi4xUXM4TUFRQUFBQUFBUUFMNTN5VWVEQmNBQUFCaEFsVk5wYzNfV2dEbDE2TkJhR'
                     '05sUVJ0SUtsRkNYNnlNa3o0Wjl3|1511161765|4581d6fb93053c5c608ffee2360a662d50cdd24c',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/62.0.3202.94 Safari/537.36',
    'X-UDID': 'AEAC-d8lHgyPTsmlNJika5gfGFulFSN2B88='
}

user_data = []


def get_user_data(page):
    for i in range(page):
        url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followers?include=data%5B*%5D.answer_count%2Cartic' \
              'les_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%' \
              '5D.topics&offset={}&limit=20'.format(i*20)
        # 抓取URL下的data数据
        response = requests.get(url, headers=headers).json()['data']
        # 把response数据添加进user_data
        user_data.extend(response)
        print('正在爬取第%s页' % str(i+1))
        # 设置爬取网页的时间间隔为5秒
        time.sleep(1)


if __name__ == '__main__':
    get_user_data(100)
    df = pd.DataFrame.from_dict(user_data)
    df.to_csv('zhihu_fans.csv')

