# _*_ coding: utf-8 _*_
import json
import re
from lxml import etree
import requests
import time

class Lagou(object):
    def __init__(self):
        # 构建初始url
        self.url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false&isSchoolJob=0'
        # 构建请求头,lg需要设置登录cookie,登录后浏览器检查工具获得即可,referer为跳转网页,也可以独立请求跳转
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Cookie': 'user_trace_token=20170821145915-a9107b9e-9ee8-41e0-a173-590a40040ccb; LGUID=20170821145916-3f76a9e9-863e-11e7-8dfa-5254005c3644; TG-TRACK-CODE=index_search; JSESSIONID=ABAAABAAAGGABCB10595D573ACB335AE234227CD85AF899; SEARCH_ID=fab5716b7e184190a14f3eed2dca1c9a; PRE_UTM=; PRE_HOST=blog.csdn.net; PRE_SITE=http%3A%2F%2Fblog.csdn.net%2Fcherrie3%2Farticle%2Fdetails%2F52644256; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2Fshujuwajue%2F1%2F%3FlabelWords%3Dlabel; _gat=1; X_HTTP_TOKEN=dd9935cb7278f1e0e17b7bc89967ac9a; _putrc=91403EB1336FB7B1; login=true; unick=%E5%88%98%E5%AE%89%E6%A3%AE; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=10; index_location_city=%E6%B7%B1%E5%9C%B3; _gid=GA1.2.139666321.1511159455; _ga=GA1.2.538073542.1503298803; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1510623133,1510970313,1511159455; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1511159983; LGSID=20171120143056-5da55acc-cdbc-11e7-99b3-525400f775ce; LGRID=20171120143943-9769209d-cdbd-11e7-99b5-525400f775ce',
            'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        }
        self.pattern = re.compile(r'"positionId":(\d+)')  # 构建正则匹配用于获取urlId
        self.base_url = 'https://www.lagou.com/jobs/{}.html'
        self.file = open('lagou.json', 'w')

    def get_post_data(self, page=1):
        """获取列表页json数据"""
        print('正在登陆----')
        post_data = {
            'first': 'true',
            'pn': page,  # 页数
            'kd': 'python', # 此处可以动态修改
        }
        response = requests.post(self.url, headers=self.headers, data=post_data)
        print('获取得列表页响应')
        return response.content.decode()

    def get_page(self, url):
        """获取详情页响应数据"""
        response = requests.post(url, headers=self.headers)
        return response.content

    def parse_url(self, data):
        """解析列表页数据获取urlid"""
        print('开始解析列表页数据,获取id')
        id_list = self.pattern.findall(data)
        url_list = []
        for id in id_list:
            url_list.append(self.base_url.format(id))
        print('id获取完毕')
        return url_list

    def parse_detail_data(self, str_data):
        """解析详情页数据"""
        print('正在获取详情页数据')
        html = etree.HTML(str_data)
        data = {}
        data['name'] = html.xpath('//div/span[@class="name"]/text()')[0] if len(html.xpath('//div/span[@class="name"]/text()'))>0 else None
        data['salary'] = html.xpath('//span[@class="salary"]/text()')[0] if len(html.xpath('//span[@class="salary"]/text()'))>0 else None
        temp = html.xpath('//dd[@class="job_request"]/p[1]/span[2]/text()')[0] if len(html.xpath('//dd[@class="job_request"]/p[1]/span[2]/text()'))>0 else None
        data['city'] = temp.replace('/', '').strip()
        data['company'] = html.xpath('//div[@class="company"]/text()')[0] if len(html.xpath('//div[@class="company"]/text()'))>0 else None
        temp = html.xpath('//dd/p[1]/span[4]/text()')[0] if len(html.xpath('//div[@class="company"]/text()'))>0 else None
        data['education'] = temp.replace('/', '').strip()
        data['job_type'] = html.xpath('//dd/p[1]/span[5]/text()')[0] if len(html.xpath('//div[@class="company"]/text()'))>0 else None
        data['anvantage'] = html.xpath('//dd[@class="job-advantage"]/p/text()')[0] if len(html.xpath('//div[@class="company"]/text()'))>0 else None
        desc_list = html.xpath('//dd[@class="job_bt"]/div/p/text()')
        temp = ''
        for desc in desc_list:
            temp += desc
        data['responsibilities'] = temp.replace('\xa0', '')
        return data

    def parse_detail(self, url_list):
        """获取单页详情页数据列表"""
        print('开始拼装详情页url')
        data_list = []
        for url in url_list:
            str_data = self.get_page(url)
            # print(str_data.decode())
            data_list.append(self.parse_detail_data(str_data))
            # print(str)
        print('获取完毕')
        return data_list

    def save_data(self, data_list):
        """保存数据模块"""
        print('开始保存数据')
        for data in data_list:
            str_data = json.dumps(data, ensure_ascii=False) + ',\n'  # 将python字典转换为json字符串
            self.file.write(str_data)

    def run(self):
        """爬虫运行逻辑模块"""
        for page in range(1, 10):  # 翻页
            data = self.get_post_data(page)  # lg数据需要登陆爬取,使用post稍微安全些,大概吧
            url_list = self.parse_url(data)  # 获取详情页所需id
            data_list = self.parse_detail(url_list)  # 获取单页详情页数据列表
            # print(data_list)  # debug
            self.save_data(data_list)  # 保存数据

    def __del__(self):
        print('数据保存完毕')
        self.file.close()  # 关闭文件


if __name__ == '__main__':
    lagou = Lagou()
    lagou.run()
