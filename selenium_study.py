# 셀레늄 - 브라우저를 자동화시킬 수 있다

# * selenium => system browser => 코드로 제어하는 브라우저
# *                            => 개발자들에게 테스트를 위해
# *                            => JS 해석 => DOM, Cookie/Session
from http import cookies
from os import name
import time
from tracemalloc import DomainFilter
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import re
from requests import request
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.expected_conditions as EC

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
c = """
BUC	IoZ2ZWRzjZA7aJ81Dg7ra8TnCzQqYPUsBnirxqH40n4=
NAC	FyKTBMRV00eRA
NACT	1
NID_AUT	cnHmlQlK9kYVjDHKG4tQI4u78RK8OYJH+wkaQ8PQJMFtWcj9a+VsPPq0oe1ohyuN
nid_inf	-1154855635
NID_JST	bTD/KMPEj02kBvlKaM1SZmtX18dBje4GJDq5LRHuCQbnU+IlsKtJvfOX1esCFuUf0CXSK9BzoTq1l7OT3j4f+DbOFIuZt/BR8Equ9wnkTluZbKusX08hTUVQTGlk/geJCqNJeRs8nVouoDFOv1RX+9NvmbTrq+DygyionpQt8Is=
NID_SES	AAABv8ST4xDjwRgSYCjMYrM/DxNiHugvKis6Qa5z66nOoKcCo6g0PMMR8qS7mJQtZJxjYY6RixCumG3u25wRo/VOYnVPsxNbo7X+ClXXWkrGLZhKbYD2JUhodQbd1keYuHKBBb4fBEXun18pcj42nelHyY2wt1jIuc4b04J/CAFT+b1nMN6H0z3Arv9C9meifGZlDDR2dhgkM3Nfg9zN+HR15lmMV/o/0+dq69g0ep83O551mdAVET55PeptCG0yKTjKTCkEqFuKo6GPKGExjjae2zRDQIMrXaLQZxP3CpxZrMVwsozQ7QLiY9w2ELgPPi4Ugvj7tDBj87GpkJb1AN7zlSxeXF6Oyea0oO+JHSAWnmk4W8JNsICl9DvM4eZawjNr6/ujkhSuDAqCoEsw4iVjekT24uSUmu8fQP6x0M+LGtckYvekpVyBClpZpzw3nPiFnUsqP0f0Bm7NtilibtHjyjgyNCKTriCu2j5uKvluVOaMCZtTSlKigyLzK5zcZ70oUaNYZ9Mkyseviu0WXzRdw4N5UooIXBnQr5i5z9earXsf1Cfn3GxAHWuF8zKdY5AByBHAXyuNq0V3yPFzSz0lrG0=
nid_slevel	1
NM_media_current	PC-MEDIA-NEWSSTAND
NM_srt_chzzk	1
NNB	WQM3VTNW76CGU
PM_CK_loc	5b3cfba8eee6debe05f5d6bd00f0cae5d5f7365bdc42727e30e57a9c9883157e
SRT30	1787101110
SRT5	1787101110
"""
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

driver = Chrome(options=options)
driver.get("https://www.google.com")

driver.find_element(By.CSS_SELECTOR, "[name=q]").send_keys("원빈")
driver.find_element(By.CSS_SELECTOR, "[name=q]").send_keys(Keys.ENTER)

driver.get_cookie("NID")

cookies = {"NID": driver.get_cookie("NID")["value"]}

url = "https://www.google.com/search"
params = {"q": "동궁"}
resp = get(url, params=params, headers=HEADERS, cookies=cookies)

print(re.search(r"<title.*>(.+)</title>", resp.text).group(1))
