# 셀레늄 - 브라우저를 자동화시킬 수 있다

from http import cookies
from os import name
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import re
from requests import request
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_experimental_option("detach", True)

driver = Chrome(options=options)
driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")

form = driver.find_element(By.XPATH, "//form")
# print(form.get_attribute("action"), form.get_attribute("method"))


userid = form.find_element(By.XPATH, './/input[@id="id"]')
userpw = form.find_element(By.XPATH, './/input[@id="pw"]')

userid.clear()
userid.send_keys("ddo_yoon")
userpw.send_keys("1994jangsoyoon!")
button = form.find_element(By.XPATH, './/button[@id="loginBtn_row"]')

button.click()
# input("확인했으면 Enter를 눌러 종료하세요...")
# c = """
# NACT	1
# NID_AUT	HGdAcCtylOFt9w6xGNdgzcI5FAeL5cPkzq/UxVC/ifBXhd/MYZnZP7ZuJLnQka/B
# nid_inf	-1153745027
# NID_JST	1eFs8B3+o56+rVdvmv5+Yq1IeFzdnbxPbih+AgVhGnHxE8RD4zPdA3ALMTWtFTXBhThiDgwiw2Exvm36C2uORYA5jnk2X1byZGlc9Liyf3rokpqWEtYtCWp9mo849QKR3oTRrIv/9HWUE/BnEsNJXDujFWLnGLl0sbxAyY1nNhA=
# NID_SES	AAABuuNd7l0pBtUPIYty/RDCJyItEpB2QiaZxEGvr3H0QsXY1/YmQllVK/TFIEKkZVY38aA07nus6TcdpxaCNEHV47WUF27PRNd6rI2BAefHqSUYMXOfj+F3M8gJVctJVbLi3JJyTkLfGBWl6TenTfUNw6sMrQUNs9Xl1676wPk2WkQfZM+mMtKR6Ie+0QQkcMruUvoSAnlyQ0oIig6EcV03+jhXDc7F7+xvrHsAoiVqeqHB9+/VOKjM+3fZei5Rnmvuc+EwOdQ3sVpR7mgy8VJJVg6lJREUEU9djep6z2O+gO1m3UXCac91xdhSha1EeHpEqi1UnXbmuNwyF2ioBDaC9jcw2lW0b58yfV0EQEo8tVM1JRNEVD6pFI+eGXK1YsJnGsqv5U/KBX5gDCL+WDWucqQ6wpZyyMKZP+kURyx2S2CrJXMjfIKEnO3OFKsoSnLlxbWjtdgqO20V9chWqzN08Yo6yY4wfaIeGiVgrsgGGc8XL8k/stI+2se3bNynBkE3pKmk6cLP+ImkLvOMk8xv6AWV9JBmDw8G9x5vWDK+T3iN4UkDfowiIrFHnXJkjGOZ2e9YBgJnzG752Id2S2oSNaA=
# nid_slevel	1
# NMUSER	JwnlKqEwaq2sKoMdaxM/pz3TBX0TWr/sKxb/FqgwFoKraxn9KxUmaqgsaqRJaqtlFoKlKqR5+6wnaZdsHoKma9vsxonOaxRpa9vs6xRpaqRVaqns1rejL9Us6xRVaqnD16lvpB2RFVl5WLl5MBp0bSloWrdnaAvmKARqp6FTW43CbNvR16lvpB2RFVl5WLl5MBp0bSloWrdnaAvmKAn=
# NNB	57IZ6QEQ45XWU
# page_uid	jo6Nadqos5wssRv3MXK-089971
# SRT30	1787015713
# SRT5	1787016350
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
