#-*- coding:utf-8 -*-
import json
import requests
import xlwt
import time
from lxml import etree

# 解决编码的问题
import sys
import importlib
importlib.reload(sys)

# 获取存储职位信息的json对象，遍历获得公司名、福利待遇、工作地点、学历要求、工作类型、发布时间、职位名称、薪资、工作年限


def get_json(url, datas):

    my_headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/60.0.3112.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_iOS?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
    }
    cookies = {
        'Cookie': 'user_trace_token=20170821145915-a9107b9e-9ee8-41e0-a173-590a40040ccb; LGUID=20170821145916-3f76a9e9-863e-11e7-8dfa-5254005c3644; JSESSIONID=ABAAABAABEEAAJA3063531735537BB84A43E6DEF2D2C2E2; _putrc=91403EB1336FB7B1; login=true; unick=%E5%88%98%E5%AE%89%E6%A3%AE; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=10; TG-TRACK-CODE=search_code; LGSID=20171122091027-ecf527a8-cf21-11e7-9cc2-525400f775ce; LGRID=20171122095800-91cbcbed-cf28-11e7-9ccc-525400f775ce; _gid=GA1.2.2052146106.1511256105; _gat=1; _ga=GA1.2.538073542.1503298803; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1510623133,1510970313,1511159455,1511256107; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1511315940; SEARCH_ID=c1aac000958140cd8bbdcac829371f45; index_location_city=%E6%B7%B1%E5%9C%B3',
    }
    time.sleep(8)
    content = requests.post(url=url, cookies=cookies, headers=my_headers, data=datas)
    # content.encoding = 'utf-8'
    result = content.json()
    print(result)
    info = result['content']['positionResult']['result']
    # print info
    info_list = []
    for job in info:
        information = []
        information.append(job['positionId'])   # 岗位对应ID
        information.append(job['companyFullName'])  # 公司全名
        information.append(job['companyLabelList'])     # 福利待遇
        information.append(job['district'])     # 工作地点
        information.append(job['education'])    # 学历要求
        information.append(job['firstType'])    # 工作类型
        information.append(job['formatCreateTime'])     # 发布时间
        information.append(job['positionName'])     # 职位名称
        information.append(job['salary'])   # 薪资
        information.append(job['workYear'])     # 工作年限
        info_list.append(information)
        # 将列表对象进行json格式的编码转换,其中indent参数设置缩进值为2
        print (json.dumps(info_list, ensure_ascii=False, indent=2))
        print (info_list)
    return info_list


def main():
    page = int(input('请输入你要抓取的页码总数：'))
    # kd = raw_input('请输入你要抓取的职位关键字：')
    # city = raw_input('请输入你要抓取的城市：')

    info_result = []
    title = ['岗位id','公司全名','福利待遇','工作地点','学历要求','工作类型','发布时间','职位名称','薪资','工作年限']
    info_result.append(title)
    for x in range(1,page+1):
        url = 'https://www.lagou.com/jobs/positionAjax.json?&needAddtionalResult=false'
        datas = {
            'first': True,
            'pn': x,
            'kd': 'python',
            'city': '上海'
        }
        info = get_json(url,datas)
        info_result = info_result+info
        # 创建workbook,即excel
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建表,第二参数用于确认同一个cell单元是否可以重设值
        worksheet = workbook.add_sheet('lagouzp',cell_overwrite_ok=True)
        for i, row in enumerate(info_result):
            # print row
            for j,col in enumerate(row):
                # print col
                worksheet.write(i,j,col)
        workbook.save('lagouzp.xls')


if __name__ == '__main__':
    main()
