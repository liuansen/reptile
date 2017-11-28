# _*_ coding: utf-8 _*_

'''
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('http://www.baidu.com')
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.baidu.com")

elem = driver.find_element_by_xpath('//*[@id="kw"]')
elem.send_keys("安森", Keys.ENTER)
# 打印网页源码
print(driver.page_source)
