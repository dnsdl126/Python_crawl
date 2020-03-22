from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from bs4 import BeautifulSoup
import requests
import cx_Oracle
import os

# DB연결
connection = cx_Oracle.connect('java/1234@localhost:1521/xe')
os.environ["NLS_LANG"] = ".AL32UTF8"
cur=connection.cursor() #cursor 함수의 연결을 사용하는 새로운 객체
                        # sql 질의를 수행하고 결과를 얻는 객체


#webdriver 설정
driver = webdriver.Chrome('C:\javazip\chromedriver.exe')
# 웹자원을 (최대)5초 기다리기
driver.implicitly_wait(5)


driver.get("https://www.idus.com/c/region/101")
driver.maximize_window()
html = driver.page_source


# for문을 이용해 3번 스크롤
# 스크롤의 길이만큼 3번 반복 하여 스크롤 다운
for i in range(3):
    driver.execute_script('window.scrollBy(0,1000)')
    time.sleep(2)


pageString = driver.page_source
soup = BeautifulSoup(pageString, 'html.parser')
#페이지에 있는 소스 내용을 받을 수 있음


section = soup.select("div.ui_card--white")
for one in section:
    c = one.find('span')
    t = one.select('a')[1]
    cont = one.select('a')[2]
    city = c.text.strip().encode('euc-kr', 'ignore').decode('euc-kr')
    title = t.text.strip().encode('euc-kr', 'ignore').decode('euc-kr')
    content = cont.text.strip().encode('euc-kr', 'ignore').decode('euc-kr')
    # 파이썬3는 기본 문자열이 Unicode 여서 한글 바로 사용가능
    # 2Byte로 하나의 문자를 표현시 모두 Unicode라고 불릴수 잇음
    # ecu-kr 유니코드가 사용되었는 데 웹크롤링된 Document에서
    # 위 코덱으로 해석이 불가능한 문자가 껴있어서 변환필요
    # encode : 유니코드 문자열을 enc-kr 문자열을 Byte로 변환 , 변환 불가능한 문자는 ignore(무시)
    # decode : 변환된 Byte를 문자열로 반환

    query = "insert into tbl_idus VALUES(:city, :title, :content)"
    db = connection.cursor()
    db.execute(query, city=city, title=title, content=content)
    connection.commit()