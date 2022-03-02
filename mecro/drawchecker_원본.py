from selenium import webdriver
import sys, os
from bs4 import BeautifulSoup, element
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/93.0.4577.82 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')
# options.add_argument('--headless')
# options.add_argument("--window-size = 1920,1080")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-running-insecure-content')
# options.add_argument("--disable-extensions")
# options.add_argument("--proxy-server = 'direct : //'")
# options.add_argument("--proxy-bypass-list = *")
options.add_argument("--start-maximized") 
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(r'./chromedriver', options=options)

#계정1
def sendID1():
    xpath = driver.find_element_by_xpath('//*[@id="j_username"]')
    xpath.send_keys("")

    xpath2 = driver.find_element_by_xpath('//*[@id="j_password"]')
    xpath2.send_keys("")
#계정2
def sendID2():
    xpath = driver.find_element_by_xpath('//*[@id="j_username"]')
    xpath.send_keys("")

    xpath2 = driver.find_element_by_xpath('//*[@id="j_password"]')
    xpath2.send_keys("")

def loginclick():
    driver.find_element_by_xpath('/html/body/section/section/div/div/div[2]/div/div[2]/div/button').click()
    
def parsing():
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    divs = soup.find_all(class_='order-list')

    for div in divs:
        result = div.find('span', class_="btn-order-detail thedraw").text.strip()
        name = div.find('span', class_="tit").text.strip()
        size = div.find('span', class_="opt").text.strip()

        if result in "당첨":
            print(name, size,"/", result)
        # else:
        #     result in "미당첨" 
        #     print(name, size,"/", result) 


print("-----------------계정1--------------------------")
# driver.delete_all_cookies()
driver.get('https://www.nike.com/kr/ko_kr/account/theDrawList')

sendID1()
loginclick()
parsing()

driver.get('https://www.nike.com/kr/ko_kr/logout')
################################################################################
print("-----------------계정2------------------------")

driver.get('https://www.nike.com/kr/ko_kr/account/theDrawList')

sendID2()
loginclick()
parsing()

driver.quit()
os.system('pause')