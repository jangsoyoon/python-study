# 셀레늄 - 브라우저를 자동화시킬 수 있다

# * selenium => system browser => 코드로 제어하는 브라우저
# *                            => 개발자들에게 테스트를 위해
# *                            => JS 해석 => DOM, Cookie/Session
from http import cookies
from os import name
import time
from tracemalloc import DomainFilter
from urllib.parse import parse_qsl
from bs4 import BeautifulSoup
from numpy import delete
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import re
from requests import request
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.expected_conditions as EC
from requests.compat import *

from config import HEADERS

options = Options()
options.add_experimental_option("detach", True)

# driver = Chrome(options=options)
# driver.get("https://www.naver.com")

# form = driver.find_element(By.XPATH, "//form")
# # print(form.get_attribute("action"), form.get_attribute("method"))


# userid = form.find_element(By.XPATH, './/input[@id="id"]')
# userpw = form.find_element(By.XPATH, './/input[@id="pw"]')

# userid.clear()
# userid.send_keys("ddo_yoon")
# userpw.send_keys("1994jangsoyoon!")
# button = form.find_element(By.XPATH, './/button[@id="loginBtn_row"]')

# button.click()
# input("확인했으면 Enter를 눌러 종료하세요...")
# c = """
# BUC	IoZ2ZWRzjZA7aJ81Dg7ra8TnCzQqYPUsBnirxqH40n4=
# NAC	FyKTBMRV00eRA
# NACT	1
# NID_AUT	cnHmlQlK9kYVjDHKG4tQI4u78RK8OYJH+wkaQ8PQJMFtWcj9a+VsPPq0oe1ohyuN
# nid_inf	-1154855635
# NID_JST	bTD/KMPEj02kBvlKaM1SZmtX18dBje4GJDq5LRHuCQbnU+IlsKtJvfOX1esCFuUf0CXSK9BzoTq1l7OT3j4f+DbOFIuZt/BR8Equ9wnkTluZbKusX08hTUVQTGlk/geJCqNJeRs8nVouoDFOv1RX+9NvmbTrq+DygyionpQt8Is=
# NID_SES	AAABv8ST4xDjwRgSYCjMYrM/DxNiHugvKis6Qa5z66nOoKcCo6g0PMMR8qS7mJQtZJxjYY6RixCumG3u25wRo/VOYnVPsxNbo7X+ClXXWkrGLZhKbYD2JUhodQbd1keYuHKBBb4fBEXun18pcj42nelHyY2wt1jIuc4b04J/CAFT+b1nMN6H0z3Arv9C9meifGZlDDR2dhgkM3Nfg9zN+HR15lmMV/o/0+dq69g0ep83O551mdAVET55PeptCG0yKTjKTCkEqFuKo6GPKGExjjae2zRDQIMrXaLQZxP3CpxZrMVwsozQ7QLiY9w2ELgPPi4Ugvj7tDBj87GpkJb1AN7zlSxeXF6Oyea0oO+JHSAWnmk4W8JNsICl9DvM4eZawjNr6/ujkhSuDAqCoEsw4iVjekT24uSUmu8fQP6x0M+LGtckYvekpVyBClpZpzw3nPiFnUsqP0f0Bm7NtilibtHjyjgyNCKTriCu2j5uKvluVOaMCZtTSlKigyLzK5zcZ70oUaNYZ9Mkyseviu0WXzRdw4N5UooIXBnQr5i5z9earXsf1Cfn3GxAHWuF8zKdY5AByBHAXyuNq0V3yPFzSz0lrG0=
# nid_slevel	1
# NM_media_current	PC-MEDIA-NEWSSTAND
# NM_srt_chzzk	1
# NNB	WQM3VTNW76CGU
# PM_CK_loc	5b3cfba8eee6debe05f5d6bd00f0cae5d5f7365bdc42727e30e57a9c9883157e
# SRT30	1787101110
# SRT5	1787101110
# """
# # * 브라우저에서 로그인을 했다는 가정하에, application-cookie-쿠키 => dict
# cookie = dict([line.split()[:2] for line in c.splitlines()])
# # for k, v in cookie.items():
# #     driver.add_cookie({'name':'k', 'value':'v'})
# #     driver.get('https://mail.naver.com')
# # * 속도가 빠른, request with cookie
# resp = request(url="https://mail.naver.com", cookies=cookie, method="GET")
# re.search(r"<title>(.+)</title>", resp.text).group(1)
# driver.close()

# * Rendering: Wait
# * Explictly(명시적), Implictly(암묵적) 기다리는 것
# * 특정 대상을 기다리는 것 , 매 페이지마다 어느 정도 시간을 기다리는 것

# # * 명시적인 기다림
# wait = WebDriverWait(driver=driver, timeout=10)
# driver.implicitly_wait(10)

# driver.find_element(By.CSS_SELECTOR, "#query").clear()
# driver.find_element(By.CSS_SELECTOR, "#query").send_keys("ㅇ")
# for li in driver.find_elements(By.CSS_SELECTOR, "#greenwindowAutocompleteLayer li"):
#     print(li.text)

# print(driver.find_element(By.CSS_SELECTOR, "#atcmp_keyword li > a").text)


# keyword = driver.find_element(By.CSS_SELECTOR, "#greenwindowAutocompleteLayer li")
# wait = WebDriverWait(driver, 10)
# try:
#     wait.until(EC.visibility_of(keyword))
# except:
#     print("화면에 보이지 않음")

# cookies = dict([line.split()[:2] for line in c.splitlines() if line.strip()])
# for k, v in cookies.items():
#     driver.add_cookie({"name": k, "value": v, "domain": ".naver.com"})
# driver.refresh()

from requests import get
import re

# driver.get("https://www.naver.com")
# driver.find_element(By.CSS_SELECTOR, "#query").send_keys("원빈")
# driver.find_element(By.CSS_SELECTOR, "#query").send_keys(Keys.ENTER)

# driver.find_element(By.CSS_SELECTOR, "#lnb .tab_menu:nth-child(3) > a").click()
# driver.find_element(By.CSS_SELECTOR, "a:has(> span > mark)").click()


# driver.switch_to.window(driver.window_handles[-1])

from requests.compat import urljoin

# driver.find_element(By.CSS_SELECTOR, "#body")

# iframe = driver.find_element(By.TAG_NAME, "iframe")
# driver.switch_to.frame(iframe)

# dom = BeautifulSoup(driver.page_source, "html.parser")
# print(dom.body.text)

# * 브라우저: 윈도우들을 관리 (탭)
# * 하나의 윈도우에는 1개의 DOM만 해석할 수 있음


# * 1. 윈도우가 새롭게 뜨면 (새탭이 생길 때)
# * driver.window_handles = [window_#id1, window_#id2...]
# * driver.switch_to.window(#id)

# * 2. DOM 안에 DOM이 있을 때 (iframe)
# * 프레임 = find_element(프레임에 위치)
# * driver.switch_to.frame(프레임) => 원래의 DOM에서 다른 DOM으로 이동

# driver.execute_script('alert("안녕");')

# driver.switch_to.window(driver.window_handles[0])
# driver.close

# driver = Chrome(options=options)
# driver.get("https://www.google.com")

# driver.find_element(By.CSS_SELECTOR, "[name=q]").send_keys("원빈")
# driver.find_element(By.CSS_SELECTOR, "[name=q]").send_keys(Keys.ENTER)

# driver.get_cookie("NID")

# cookies = {"NID": driver.get_cookie("NID")["value"]}

# url = "https://www.google.com/search"
# params = {"q": "동궁"}
# resp = get(url, params=params, headers=HEADERS, cookies=cookies)

# print(re.search(r"<title.*>(.+)</title>", resp.text).group(1))

import json

with open("naver.json", "r", encoding="utf8") as fp:
    naver = json.load(fp)
    #     print(naver)

# driver = Chrome(options=options)
# driver.get("https://mail.naver.com")

# userid = driver.find_element(By.CSS_SELECTOR, "#id")

# userpw = driver.find_element(By.CSS_SELECTOR, "#pw")

# userid.clear()
# userid.send_keys(naver["id"])
# userpw.clear()
# userpw.send_keys(naver["pw"])
# driver.implicitly_wait(10)
# userpw.send_keys(Keys.ENTER)
# cookies = dict(map(lambda row: (row["name"], row["value"]), driver.get_cookies()))
c = """BUC	QTGlrPMEYeNZKFkUdvhe-czLnftYZ1om9ySk7PmSN2s=
NAC	fVyJCYCtyV5FB
NACT	1
NID_AUT	wDV+QkBib8ouJL2Rb2/uvtiDkS4cFA0RpSEnMyXVy24+sqtoxYhWVV24rfM9e1wq
NID_BRIDGE_USE	true
nid_inf	-1322489040
NID_JST	Spbo2nF75kIvSX/t0t2l/TnwkokYo0SC//ErvQRruId8md8MkQxnrLogeA59mUqGX6v+p0FJxZLb2ILmWIjrtmiNdzS20H/b8Xlrji7LSKbjoUcMq9PrHpvuHth5WcH7wlAfO88yGqUUUY8kUBbKJlNBYVo5eOYfzcHuYmy7i04=
NID_PK_BT	|HZkRtYtr7QYj3qiVX7HhvpW6+tAtJNF3eBZtvXtpU1c=
NID_SES	AAABmMjMjyUHWX5cCLp6gAl71ST0+CRDZAlQxq5Uj5sVrgaT9xM67cDgN2dAyO5XRehkh7ATrKaNqfbMQtfQGaZgGrkJSZojQUal63HZT8fm168KvnT2ED7yyT3pzSLmQhwOftQFUabUVybIg+9OfpfBA8FkaLvfDQKy5TyQEAP9cWTcI24m4eH8hYEe0bxagR29C0k5sj8ouAT4hZH5+GGEmRukYhetkEF4Ar1rIBTs+UgFkhnm5jK/C7TV4GL3gMmSdn51ifnjum6gt0zXmo3IL5ziuXmQWlkjSPRW4qT2yPdNrymqM2iv5DjFPiLMxf9TxPo0cW427+UTBSltvPT50E96Nw2fjd2EbjIvZTNwYX3GwaXLhQLxrlM2alcjypM2hk0g2zlgkbUxbbxNT25pol8p5k4X7WffYUBKMw49cSfPCWMr2qi6sqJ1BvRStys/1rCRu1sVkiTcx3QRLWxRx5Gv9/hkw1NjKVZVi54OU6s2FyLTLadr9ye6XFahP8W2fYjB2RVFI0JkZ7sckvV3hcTTj6RmxFkbAQC61vXStqtB
nid_slevel	1
NMUSER	U/n9aAbwaq2sFxMlaAMdWHkr+6FCMBtsKxb/FqulKqbZFAn9KxUmaqgsaqRJaqtlFotdKoR5+6wnaZdsHoKma9vsxonOaxRpa9vs6xRpaqRVaqns1rejL9Us6xRVaqnD16lvpB2RFLl5WLl5MBp0bSloWrdnaAvmKARqp6FTW43CbNvR16lvpB2RFLl5WLl5MBp0bSloWrdnaAvmKAn=
NNB	A72LLHTENGDGU
SRT30	1787193700
SRT5	1787193700
"""

cookies = dict([line.split()[:2] for line in c.splitlines()])

# 여기까지가 셀레늄으로 쿠키만 받아오는 과정
# print(cookies)

# url = "https://mail.naver.com"

# resp = request(url=url, cookies=cookies, headers=HEADERS, method="GET")
# print(re.search(r"<title.*>(.+)</title>", resp.text).group(1))  # type: ignore

# params = json.loads(
#     '{"article":{"cafeId":"31766964","contentJson":"","from":"pc","menuId":1,"subject":"아무거나4","tagList":[],"editorVersion":4,"parentId":0,"open":false,"naverOpen":true,"externalOpen":true,"enableComment":true,"enableScrap":true,"enableCopy":true,"useAutoSource":false,"cclTypes":[],"useCcl":false}}'
# )
# params["article"]["contentJson"] = json.loads(
#     '{"document":{"version":"2.10.2","theme":"default","language":"ko-KR","id":"01M0EAZGA9MD40F5NDJ2MVPBBX","components":[{"id":"SE-b8262476-1a7c-475b-8a2c-07023442f61e","layout":"default","value":[{"id":"SE-b863196a-e111-4788-bd73-dd2bd119e0f1","nodes":[{"id":"SE-c3c22198-3581-4b08-a960-6aca86d5b17d","value":"아무거나4","@ctype":"textNode"}],"@ctype":"paragraph"}],"@ctype":"text"}],"di":{"dif":false,"dio":[{"dis":"N","dia":{"t":0,"p":0,"st":9,"sk":2}},{"dis":"N","dia":{"t":0,"p":0,"st":9,"sk":2}}]}},"documentId":""}'
# )

# params["article"]["contentJson"]["document"]["components"][0]["value"][0]["nodes"][0][
#     "value"
# ] = "새 글 테스트"
# params["article"]["subject"] = "새 글 테스트222"

# params["article"]["contentJson"] = json.dumps(params["article"]["contentJson"])

# url = "https://apis.cafe.naver.com/editor/v2.0/cafes/31766964/menus/1/articles"

# request(url=url, json=params, cookies=cookies, headers=HEADERS, method="POST")


# url = "https://apis.naver.com/cafe-web/cafe-boardlist-api/v1/cafes/31766964/menus/1/articles?page=1&pageSize=15&sortBy=TIME&viewType=L"
# url, params = url.split("?")
# params = dict(parse_qsl(params))
# articleList = []
# for i in range(1, 15):
#     params["page"] = i  # type: ignore
#     resp = request(url=url, params=params, method="GET")
#     # print(resp.json()["result"]["articleList"])
#     print(i, len(resp.json()["result"]["articleList"]))

#     articleList.extend(
#         list(
#             filter(
#                 lambda data: data["item"]["writerInfo"]["nickName"] == "8기장소윤",
#                 resp.json()["result"]["articleList"],
#             )
#         )
#     )
#     if len(resp.json()["result"]["articleList"]) < 15:
#         break

# print(articleList)

# url = "https://apis.naver.com/cafe-web/cafe-mobile/ArticleDelete.json"
# params = dict(parse_qsl("cafeId=31766964&articleId=52&requestFrom=A"))

# for article in articleList:
#     pid = params["articleId"] = article["item"]["articleId"]
#     print(pid)
#     HEADERS["referer"] = (
#         f"https://cafe.naver.com/ca-fe/cafes/31766964/articles/{pid}?menuid=1&referrerAllArticles=false&page=1&boardtype=L&fromNext=true"
#     )
#     resp = request(
#         url=url, data=params, cookies=cookies, headers=HEADERS, method="POST"
#     )

#     print(resp.text)


# ! 인증받지 않은 공식 API를 활용하여
# ! 특정 파라미터와 주소를 통해 자동으로 정보를 요청하고 삭제하는 방법 연습 해보기
# ! (a.k.a. 카페에 자동으로 글 쓰고 삭제하고 튀기 -> 특정 글에 코멘트 쓰고 삭제하고 튀기)


################# 댓글 달기 ##################
create_url = "https://apis.naver.com/cafe-web/cafe-mobile/CommentPost.json"
delete_url = "https://apis.naver.com/cafe-web/cafe-mobile/CommentDelete.json"

params = dict(
    parse_qsl("content=d&stickerId=&cafeId=31766964&articleId=85&requestFrom=A")
)
# for i in range(0, 10):
#     params["content"] = f"댓글 도배{i}번째"
#     HEADERS["referer"] = (
#         "https://cafe.naver.com/ca-fe/cafes/31766964/articles/85?menuid=1&referrerAllArticles=false&page=2&boardtype=L&fromNext=true"
#     )
#     time.sleep(2)
#     resp = request(url=create_url, cookies=cookies, data=params, headers=HEADERS, method="POST")  # type: ignore

# ########바로 댓글 삭제#######
# resp_data = json.loads(resp.text)
# comment_id = resp_data["commentId"]
# params["commentId"] = comment_id
# time.sleep(2)
# request(
#     url=delete_url, cookies=cookies, headers=HEADERS, data=params, method="POST"
# )
# # cafeId=31766964&menuId=1&articleId=85&commentId=114493945&requestFrom=A
# print(resp.text)

########## 댓글 전체 삭제 ##########
# 1. 일단 내 댓글들 다 리스트 불러오기
# comment_id_list = []
# get_url = "https://article.cafe.naver.com/gw/v4/cafes/31766964/articles/85?query=&menuId=1&boardType=L&useCafeId=true&requestFrom=A"
# resp = request(url=get_url, cookies=cookies, method="GET")
# resp_data = json.loads(resp.text)
# for item in resp_data["result"]["comments"]["items"]:
#     if item["writer"]["nick"] == "8기장소윤":
#         ######## 여기에서 확인 필요
#         # print(item["id"])
#         comment_id_list.append(item["id"])

# # 2. 리스트 돌면서 하나씩 삭제하기
# # print(comment_id_list)
# for comment_id in comment_id_list:
#     params["commentId"] = comment_id
#     time.sleep(2)
#     request(
#         url=delete_url, cookies=cookies, headers=HEADERS, data=params, method="POST"
# )
# cafeId=31766964&menuId=1&articleId=85&commentId=114493945&requestFrom=A
