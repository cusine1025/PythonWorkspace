from selenium import webdriver
import sys, os
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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

driver = webdriver.Chrome('C:\chromedriver', options=options)

#https://www.nike.com/kr/launch/t/men/fw/basketball/DN4904-001/ydwk92/air-jordan-1-mid-se
URL = "https://www.nike.com/kr/launch/t/women/fw/nike-sportswear/CI0919-113/mwqc31/w-af1-shadow"
def getURL():
    driver.get(URL)

#계정1
def sendID1():
    driver.find_element_by_xpath('//*[@id="jq_m_right_click"]/div/ul/li[2]/a').click()

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='j_username']"))).send_keys("kisoo0423@daum.net")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='j_password']"))).send_keys("kisoo0423@")

    driver.find_element_by_xpath('//*[@id="common-modal"]/div/div/div/div/div[2]/div/div[2]/div/button').click()
#계정2
def sendID2():
    driver.find_element_by_xpath('//*[@id="jq_m_right_click"]/div/ul/li[2]/a').click()

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='j_username']"))).send_keys("")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='j_password']"))).send_keys("")

    driver.find_element_by_xpath('//*[@id="common-modal"]/div/div/div/div/div[2]/div/div[2]/div/button').click()

def autobuy():
    time.sleep(1)
    size = Select(driver.find_element_by_id('selectSize'))
    #size.select_by_visible_text('240')
    try:
        size.select_by_visible_text('250')
    except:
        size.select_by_visible_text('235')

    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="btn-buy"]').click()

    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="btn-next"]').click()

    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="payment-review"]/div[1]/ul/li[1]/div/div[2]/h6').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="payment-review"]/div[1]/ul/li[2]/form/div/span').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="complete_checkout"]/button').click()


print("-----------------계정1--------------------------")
# driver.delete_all_cookies()

getURL()
sendID1()
try:
    autobuy() ,print("SUCCESS!")
except:
    print("FAIL")
  
#driver.get('https://www.nike.com/kr/ko_kr/logout')
################################################################################
#print("-----------------계정2------------------------")

#getURL()
#sendID2()
#try:
#    autobuy() ,print("SUCCESS!")
#except:
#    print("FAIL")
#driver.quit()
os.system('pause')
