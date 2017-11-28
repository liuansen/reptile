# _*_ coding: utf-8 _*_
__author__ = 'Anson'
import requests
from lxml import etree


url = 'http://xm.xiaozhu.com/'
r = requests.get(url).text
s = etree.HTML(r)
# 短租标题
print(s.xpath('//*[@id="page_list"]/ul/li/div[2]/div/a/span/text()'))
# 短租价格
print(s.xpath('//*[@id="page_list"]/ul/li/div[2]/span[1]/i/text()'))
# 经纬度
print(s.xpath('//*[@id="page_list"]/ul/li/text()'))
