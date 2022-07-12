# selenium 라이브러리에서 크롬 웹드라이버 가져오기
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('C:\\chromedriver')

driver.get('https://stdict.korean.go.kr/search/searchView.do?word_no=169066&searchKeywordTo=3')

# 메뉴 화면의 급식 게시판 1번째 클릭
text = driver.find_element(By.XPATH, '//*[@id="word_169066"]/p[3]').text

print(text)
