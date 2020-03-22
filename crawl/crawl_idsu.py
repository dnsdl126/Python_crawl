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

    query = "insert into tbl_idus VALUES(:city, :title, :content)"
    db = connection.cursor()
    db.execute(query, city=city, title=title, content=content)
    connection.commit()