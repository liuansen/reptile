import requests
r = requests.get('https://www.xmrc.com.cn/net/info/resultg.aspx?PageIndex=1').text

from bs4 import BeautifulSoup
soup = BeautifulSoup(r, 'lxml')
pattern = soup.find_all('a', 'a4 bold')
for item in pattern:
    print(item.string)

import pandas
comments = []
for item in pattern:
    comments.append(item.string)
df = pandas.DataFrame(comments)
df.to_csv('comments.csv')
