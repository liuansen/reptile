# _*_ coding: utf-8 _*_
import requests
import pandas as pd
import time

headers = {
    'authorization': 'Bearer 2|1:0|10:1510715159|4:z_c0|80:MS4xUXM4TUFRQUFBQUFtQUFBQVlBSlZUUmY5LUZvUnlHR1luRXZtamlmQk5'
                     'ZNnZXbUcwNElLUHZnPT0=|29206a8a39a9d5b11f6536e43080571694197225f6d115ed851fcf70e0d37ae6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.'
                  '0.2987.98 Safari/537.36',
}

user_data = []
def get_user_data(page):
    for i in range(page):
        url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_coun' \
              't%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(typ' \
              'e%3Dbest_answerer)%5D.topics&offset={}&limit=20'.format(i*20)
        response = requests.get(url, headers=headers).json()['data']
        user_data.extend(response)
        print("正在爬取第%s" % str(i+1))
        time.sleep(10)


if __name__ == '__main__':
    get_user_data(10)
    df = pd.DataFrame.from_dict(user_data)
    df.to_csv('users.csv')
