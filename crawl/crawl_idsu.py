from bs4 import BeautifulSoup
import requests
import cx_Oracle
import os
import chardet
import urllib
connection = cx_Oracle.connect('java/1234@localhost:1521/xe') #DB연결
os.environ["NLS_LANG"] = ".AL32UTF8"
cur=connection.cursor() #cursor 함수의 연결을 사용하는 새로운 객체
                        # sql 질의를 수행하고 결과를 얻는 객체


r= requests.get("https://www.idus.com/c/region/101") #url로부터 데이터 저장
print(r.encoding)


plain_text = r.text #source_code의 텍스트 부분만  plain_text 저장

soup =BeautifulSoup(plain_text, 'html.parser') #가독성을 위해 변수 soup에 저장

section = soup.select("div.ui_card--white")
for one in section:
    city = one.find('span').getText().encode('euc-kr','ignore').decode('euc-kr')
    title = one.select('a')[1].getText().encode('euc-kr','ignore').decode('euc-kr')
    content = one.select('a')[2].getText().encode('euc-kr','ignore').decode('euc-kr')
    #파이썬3는 기본 문자열이 Unicode 여서 한글 바로 사용가능
    #2Byte로 하나의 문자를 표현시 모두 Unicode라고 불릴수 잇음
    # ecu-kr 유니코드가 사용되었는 데 웹크롤링된 Document에서
    # 위 코덱으로 해석이 불가능한 문자가 껴있어서 변환필요
    # encode : 유니코드 문자열을 enc-kr 문자열을 Byte로 변환 , 변환 불가능한 문자는 ignore(무시)
    # decode : 변환된 Byte를 문자열로 반환

    query = "insert into tbl_idus VALUES(:city, :title, :content)"
    db = connection.cursor()
    db.execute(query, city=city, title=title, content=content)
    connection.commit()


# for x in cur: # for 변수 in list = list 요소들을 x에 담는다
#     print(x)
    # connection.close() ('서울', '요리', '재밌네요')

