#!/bin/env python2.7

# Uses a webdriver
# Place chrome driver binary on Desktop
# Binary used here: https://www.sendspace.com/file/b5bkei
import os, requests
from selenium import webdriver
from requests.utils import dict_from_cookiejar
tokenContainer=[]

driverBin=os.path.expanduser("~/Desktop/chromedriver")
driver=webdriver.Chrome(driverBin)

# Page you solve captcha on - this isn't the proguct being added
# This will need ot be changed - other captcha product
driver.get('http://www.adidas.com/us/tubular-doom-shoes/S74791.html')

# Go to first iframe
# BaseToken always has frame name = 'undefined'
driver.switch_to_frame('undefined')

# Grab BaseToken in this frame
token_value = driver.find_element_by_id('recaptcha-token').get_attribute('value')

# Go back to top view
driver.switch_to_default_content()

# print token_value
print 
print 'User must solve Captcha!!'
print 'Come back to this terminal once it has been solved and press Enter'
print

# Waiting fo user to solve captcha then hit enter
raw_input('')

# Solve of captcha creates second frame with solve token - go to it
# This frame has random string as name
# On adidas - last frame indexed (7) or [6] - 0 inclusive
count=0
flag=True
while flag==True:
	driver.switch_to.frame(count)
	try:
		tokenContainer.append(driver.find_element_by_id('recaptcha-token').get_attribute('value'))
		if len(tokenContainer)>1:
			flag=False
	except:
		pass
	driver.switch_to_default_content()
	count+=1

new_token_value= tokenContainer[-1]
# Go back to top view

driver.switch_to_default_content()
print new_token_value
print 

# Ensure that we're back at the top
# print driver.page_source


##############
#ADDED
##############
driver.quit()


session=requests.session()
session.cookies.clear();
url='http://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-MiniAddProduct'

# This is the captcha product to be added
pid='BA8296'
print 'Injecting replacement product id:',pid

headers={
	'Accept':'*/*',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'en-US,en;q=0.8',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Host':'www.adidas.com',
	'Origin':'http://www.adidas.com',
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest'
}

# Change pid key's value with 3 digit size code
# 670 equates to size 11US
payload={
	'layer':'Add To Bag overlay',
	'pid':pid+'_670',
	'Quantity':'1',
	'g-recaptcha-response':new_token_value,
	'masterPid':pid,
	'ajax':'true'
}


res=session.post(url,data=payload,headers=headers)
# print res.status_code
# print res.content


cookies = dict_from_cookiejar(res.cookies)
driver=webdriver.Chrome(driverBin)
driver.get('https://www.adidas.com/on/demandware.store/Sites-adidas-US-Site/en_US/Cart-Show')
driver.delete_all_cookies()
for key, value in cookies.items():
    driver.add_cookie({'name': key, 'value': value})
driver.refresh()
print

# Do your thing and checkout