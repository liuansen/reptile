import requests
from lxml import etree

url = 'https://book.douban.com/subject/1084336/comments/'
r = requests.get(url).text

s = etree.HTML(r)
file = s.xpath('//div[@class="comment"]/p/text()')
print(file)

"""
import pandas as pd
df = pd.DataFrame(file)
df.to_excel('pinglun.xlsx')
"""

