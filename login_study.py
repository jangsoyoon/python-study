from sqlite3 import paramstyle
from urllib.parse import parse_qsl
from requests.compat import urljoin
from requests import get, request
import re
from config import HEADERS

# Cookie / Session

#! Client ------> ID/PW ----------> Server[URI;mail.naver.com]
#!        <-------------- Response
#! Client ------> Request
#!        <-------------- Loggedin - OK 제공 아니면 X

#! Cookie(웹)                  Session(서버)

from bs4 import BeautifulSoup

# url = "https://pythonscraping.com/pages/login.html"
# resp = get(url)
# dom = BeautifulSoup(resp.text, "html.parser")
# url = urljoin(url, dom.select_one("form").attrs["action"])
# method = dom.select_one("form").attrs["method"]
# params = [tag.attrs["name"] for tag in dom.select_one("form").select("input[name]")]
# resp = request(url=url, data={k: k for k in params}, method=method)

# print(resp.request.body)
# print(
#     dom.select_one("form").attrs["action"],
#     dom.select_one("form").attrs["method"],
#     [tag.attrs["name"] for tag in dom.select_one("form").select("input[name]")],
# )


# url = "https://mail.naver.com"
# resp = get(url)
# dom = BeautifulSoup(resp.text, "html.parser")

# print(
#     dom.select_one("form").attrs["action"],
#     dom.select_one("form").attrs["method"],
#     [tag.attrs["name"] for tag in dom.select_one("form").select("input[name]")],
# )


url = "https://www.scrapingcourse.com/login"
resp = get(url)
dom = BeautifulSoup(resp.text, "html.parser")
# print(
#     dom.select_one("form").attrs["action"],
#     dom.select_one("form").attrs["method"],
#     [tag.attrs["name"] for tag in dom.select_one("form").select("input[name]")],
# )
url = urljoin(url, dom.select_one("form").attrs["action"])
method = dom.select_one("form").attrs["method"]
# params = {"email": "admin@example.xom", "password": "password"}
# resp = request(url=url, method=method, data=params)

# print(resp.request.url, resp.request.body)
# BeautifulSoup(resp.text, "html.parser").title
# cookie = resp.headers["set-cookie"]

# headers = {"cookie": cookie}
# resp = get(resp.request.url, headers=headers)
# print(resp.request.url, re.search("<title>(.+)</title>", resp.text).group(1))
# resp = request(url=url, data={k: k for k in params}, method=method)
from requests.sessions import Session

session = Session()


# params = {"email": "admin@example.xom", "password": "password"}
# resp = session.request(url=url, method='POST', data=params)
# print(resp.request.url, re.search("<title>(.+)</title>", resp.text).group(1))

# print(resp.headers["set-cookie"], session.cookies)

url = "https://www.scrapingcourse.com:443/dashboard"
resp = request(url=url, method="GET")
# print(resp.request.url, re.search("<title>(.+)</title>", resp.text).group(1))


# url = "https://www.scrapingcourse.com:443/dashboard"
# resp = session.request(url=url, method="GET")
# print(resp.request.url, re.search("<title>(.+)</title>", resp.text).group(1))


# session.cookies.clear()
# c = """
# _fbp	fb.1.1786330551823.878653426350046685	.naver.com	/	2026-11-08T02:55:51.000Z	41			Lax			Medium
# ASID	a39803c90000019fd487fae400000020	.naver.com	/	2027-09-10T00:45:09.258Z	36		✓	None			Medium
# BUC	56VtGVvd10bCiig8fqIVSURs_vhQTEuDCMbAyjxIzQc=	.naver.com	/	2027-09-18T07:23:33.102Z	47	✓	✓	None			Medium
# cto_bundle	HRlCK19FdzhvZHRraFVKd2hCVVJNN2RVMEhxc3E4RndmQ0J3U1olMkI0ajBGM0s2d0Rnd2VBTUpDNkc0ayUyQlYySURmTmhFT2lHbHJJdlBxU2pDMjgza0I0dzVWU1JlMzF4cGZQUHl1NUxJaHBxbk1Zc1VpczVFTVlneERIZnVDMWM1QjU4JTJCcUR3WHVSeW9DN3U5bENNcGxIaWZ6WGclM0QlM0Q	.naver.com	/	2027-09-06T18:27:04.000Z	233						Medium
# NAC	LFoGBMhAOjf2A	.naver.com	/	2027-09-18T00:00:02.189Z	16		✓	None			Medium
# NACT	1	.naver.com	/	2026-08-15T00:00:02.359Z	5						Medium
# NID_AUT	fKrRpdTwmwkMc8okfJhBRfowUXoWDsg/k1gXyfY+BHX5uSwv5JD3RsXSyYgYyjw6	.naver.com	/	2026-09-06T00:55:28.461Z	71	✓	✓	Lax			Medium
# nid_inf	-1170465476	.naver.com	/	2026-09-06T00:55:28.461Z	18						Medium
# NID_JST	obbhRbzbF/an/Qq/Y+UbGtzEIX2b5ewI9eDu3m+i+aXFXZGC8y5PuYz/aomi1GaOPLDDWfYoTN/iNPqywAWE+BJ8bcwRSqQClDifJzxaq/UyAOvobyA+Uft6UkxWkET1R61K0czvEGKiLvgNFwee4Ivu2pTw0p5oNbLf/Devw1Y=	.nid.naver.com	/	2027-02-23T00:55:21.741Z	179	✓	✓	Lax			Medium
# NID_SES	AAABwNODmHYzhfxSXPb45FwKl79/hE+eZmE3VDOC38ZucjnlgHKAOHdT3zW9bcSGIlyhDjj4YFWNLwqRgMY6piiweR+kcr5fsBBMncU0nc/W6Kj+D2CInamtGQEoLK5cypedaMJDvzjupDTIrBKOwX7pYq7vmDdk6TfaAPZ72DiokPh5+FyRMvWmXD3NiFZnBwCucffkWUEJ9duq7X/cSnyhFUYoytZ5Dt2uzI2iSQQetjjnmdF87WTH/PgaYkRP/y1GWqjoDqKqtg7kN14eGF2OLYIQyorqI665eKhuEOMxI0Dsy1yPK89aDslRWACKp1jx1KRlhR0Wa9Mtgs1uUbVPXvZxzV6s94qzvCPMEI6TxCg6G1SLJmg2KlQazGHLFdhu+/tfdr+42WJasJsKBElDeiizTJJdYX/l8IB/dgaTPGg21kHVCjNRx2crWMgWup/EqC5RWgoEZFNSW/Nx9HZJ38acQ5GxjdCAxEwTLwMWslEtJhMOFrSuidK67Gq03NoIb3BAe8atuoZHqFmK8J2kdmK5G9Xz7orpbBkLnFll6Ctn6PbP+HHcmfI4sLbR3CHHnXlkdNbF0UAYCRPMYnaFbr8=	.naver.com	/	2026-09-13T07:23:33.144Z	611		✓	Lax			Medium
# nid_slevel	1	.nid.naver.com	/	2027-08-05T23:46:20.000Z	11						Medium
# NMUSER	JwnlKqEwaq2sKoMdaxM/pz3TBX0TWr/sKxb/FogrFAuZaAn9KxUmaqgsaqRJaqtlFouqFxR5+6wnaZdsHoKma9vsxonOaxRpa9vs6xRpaqRVaqns1rejL9Us6xRVaqnD16lvpB2RFVl5WLl5MBp0bSloWrdnaAvmKARqp6FTW43CbNvR16lvpB2RFVl5WLl5MBp0bSloWrdnaAvmKAn=	mail.naver.com	/	Session	218	✓	✓				Medium

# """
# cookie = dict([line.split()[:2] for line in c.splitlines() if len(line) > 0])
# for k, v in cookie.items():
#     session.cookies.set(k, v)


# url = "https://mail.naver.com/json/list?folderSN=0&page=1&viewMode=time&previewMode=1&sortField=1&sortType=0&u=ddo_yoon"
# url, params = url.split("?")
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
}
# params = dict(parse_qsl(params))
# print(params)
# params["folderSN"] = 5
# resp = session.request(url=url, params=params, method="POST", headers=headers)

# # print([mail["preview"] for mail in resp.json()["mailData"]])

# print(session.cookies.get_dict)


url = "https://www.google.com/search?q=%EC%9B%90%EB%B9%88&oq=%EC%9B%90%EB%B9%88&gs_lcrp=EgZjaHJvbWUqCAgAEEUYJxg7MggIABBFGCcYOzINCAEQABiDARixAxiABDINCAIQABiDARixAxiABDINCAMQABiDARixAxiABDINCAQQLhiDARixAxiABDIGCAUQRRg8MgYIBhBFGDwyBggHEEUYPNIBCDE2MTVqMGo3qAIAsAIA&sourceid=chrome&source=chrome.ob&ie=UTF-8"

url, params = url.split("?")
params = dict(parse_qsl(params))


# cookies = [
#     # {"AEC": "AdJVEavYPAGUp00DNbvnD-G8GOqp7s9gsKsFyTT1aUFyKuaF9T61tM77_Tw"},
#     # {"APISID": "7izjyUPGMUPIDHeJ/AmPRbvo4UziTPuTYw"},
#     # {
#     #     "DV": "o5suTmyKyeNjUHFnxQKTMX9PIXL1_5l7gAFAyE5GVAAAAFBgUOKbGI6UsQAAAISvFQ9mKv6nNQAAAAHiplD9Std3EgAAABomwfjlk8pDBgAAAA"
#     # },
#     # {"HSID": "Alyfajm9tWpF155e7"},
#     {
#         "NID": "533=Oj_SvYzs4l7luotYu2qsNf9nxbPIWHwATxwQ5naljjb9biH6mU8VIauV9yNiQsymra4nb53OCUR9pIWKt2dODpVBUjOtXsDPxXGSgx43As4eH_CIJMZT4uDz02g1demGGBONW-3J8tyf9EPR_CoLDqKKjqH7YP--_cZH3kuzNPDJjrwmrmL5gjuHHzODEo5hE4U"
#     }
#     # {
#     #     "OSID": "g.a000BgnF91JNOwSzx7lEHCJOuJShpXqlbRCksiX84hRmonfZfxFXMVx3EJfmQ2PzFIWt093qsQACgYKAQUSARISFQHGX2MiLQ91kwmy5jn4tlCnUDb5tRoVAUF8yKpftddH94yi9HD1tvybiI4I0076"
#     # },
#     # {"SAPISID": "WjliDIdPRj_PuRRm/AYmvFaHGUkhtrhf30"},
#     # {"SEARCH_SAMESITE": "CgQIx6EB"},
#     # {
#     #     "SID": "g.a000BgnF9-XQMN4C--Njq_ZIfmrG40pclkVx7DJ1ErXpvLItMoKP3iyp8W1VSCHPl40DvLQ1UwACgYKAXUSARISFQHGX2Mi3zS7wlJkppI5RJsRSPX0NBoVAUF8yKoPo1VyhYSlOkn_d__MWqYt0076"
#     # },
#     # {
#     #     "SIDCC": "AKEyXzXPlhiK563nEzCL9qdTpx8uCQUYec2nC70du8Z-laKW6nv3pltEEB69gmcDlD3ncgkn_Q"
#     # },
#     # {"SSID": "AqB3yCU5SQrUceczA"},
# ]

cookie = {
    "NID": "534=qqk1WoPHwTdz9jQ44SeHqd4Uqzr6hcVWG5Q2tfjECv6WVL9ZBqMvnYLW8iWiednM0m7JcpjE32owEkYl6vrSVqBUUvylnCZX60RvI_GExFuj96ioyqQ0XXLUW2xpe4bwBICnLEBG36tKpz4PwVKkrn4u4o9uND7-ezNhBSU1MzLUHqQ432AOkhoR6JrYWpuiUtoxjsBjlYIAUbLNh4RobjuP1zffef-cLK-8-n20GYqO7gMPXRuj24225vmoNQXOxhTjtIl0YlU"
}

# for cookie in cookies:
# resp = request(url=url, params=params, method="GET", headers=headers, cookies=cookie)
# print(cookie, re.search(r"<title>(.+)</title>", resp.text).group(1))


url = "https://www.google.com/search?q=%EC%9B%90%EB%B9%88&oq=%EC%9B%90%EB%B9%88&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg8MgYIAhBFGDwyBggDEEUYPNIBCDI1MDlqMGo3qAIAsAIA&sourceid=chrome&source=chrome.ob&ie=UTF-8&sei=NaWDatu_Jd3M1e8PiP_egA4"
# params = {"q": "원빈", "source": "chrome.ob", "sourceid": "chrome", "ie": "UTF-8"}
resp = request(url=url, headers=HEADERS, method="GET", cookies=cookie)
print(resp.text)
# print(re.search(r"<title>(.+)</title>", resp.text).group(1))
