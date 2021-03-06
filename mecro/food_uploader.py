# selenium 라이브러리에서 크롬 웹드라이버 가져오기
from selenium import webdriver
from urllib.request import urlretrieve
from ctypes import windll
from selenium.webdriver.common.keys import Keys

# 웹 드라이버 실행
driver = webdriver.Chrome('C:\\chromedriver')

# 하늘고 리로스쿨 로그인 화면 주소 입력
driver.get('https://haneul.riroschool.kr/user.php?')

driver.implicitly_wait(1)
# 로그인을 위해 아이디와 패스워드 입력
driver.find_element_by_name('id').send_keys('20211025')
driver.find_element_by_name('pw').send_keys('Rladnwls050828@')

# 로그인 버튼 클릭
login_x_path = '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/button'
driver.find_element_by_xpath(login_x_path).click()

# 메인 화면 로딩을 위해 1초 기다리기
driver.implicitly_wait(1)

try:
    # 팝업창 클릭하여 없애기
    driver.find_element_by_xpath('//*[@id="closePopup1"]').click()
except:
    pass

# 메뉴 화면의 급식 게시판 1번째 클릭
xpath = 'br.find_element_by_xpath("//*[contains(@onclick,\'3월4주 주간메뉴표\')]").click()'
driver.find_element_by_xpath(xpath).click()

# 이미지 주소가 있는 html 주소를 입력하여 이미지 주소 퍼오기
css = "#rText > div > p:nth-child(3) > img"
image = driver.find_elements_by_css_selector(css)

# 이미지 소스 가져오기
url = image.get_attribute('src')

# url에 있는 이미지를 받아오기
urlretrieve(url, "test.jpg")

# ctypes를 이용하여 바탕화면 조작
windll.user32.SystemParametersInfoW(20, 0, "C:\\Users\\gram_\\Desktop\\test.jpg" , 3)
# windll.user32.SystemParametersInfoW(20, 0, "C:\\Users\\ops500-501-H\\Desktop\\test.jpg" , 3)