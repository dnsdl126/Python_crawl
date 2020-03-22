
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#webdriver 설정
driver = webdriver.Chrome('C:\developer\chromedriver.exe')
# 웹자원을 (최대)30초 기다리기
driver.implicitly_wait(30)

url="https://www.idus.com/c/region/101"
# url 요청(주소 입력하고 Enter)
driver.get(url)

# 페이지 스크롤 다운
# 페이지의 바디 찾기
body = driver.find_elements_by_css_selector('body')

# for문을 이용해 3번 스크롤
for i in range(3):
    driver.execute_script('window.scrollBy(0,1000)')
    time.sleep(2)


#페이지에 있는 소스 내용을 받을 수 있음
pageString = driver.page_source
print(pageString)