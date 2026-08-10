from hmac import new
import json
from os import name
from re import A, ASCII, L
from urllib.request import Request, urlopen

import attr
import re._constants
from urllib3 import HTTPResponse

# resp = urlopen("https://www.naver.com")

# print(resp.getheaders())
# print(resp.read().decode("utf-8"))

# import re

# encoding = re.search("charset=(.+);?", resp.headers.get("content-type")).group(1)
# html = resp.read().decode(encoding)
# print(re.search(r"<title>(.+?)</title>", html).group(1))


from urllib.robotparser import RobotFileParser

# parser = RobotFileParser()

# parser.set_url("https://www.korea.ac.kr/robots.txt")

# parser.read()
# print(parser.can_fetch("bot", "/search/about"))

# resp = urlopen("https://www.google.com")
# print(resp.status, resp.reason, resp.getheaders())

# resp.read().decode("iso-8859-1")
from html import escape, unescape

# url = "https://www.google.com/search?q=%EC%9B%90%EB%B9%88&oq=%EC%9B%90%EB%B9%88&gs_lcrp=EgZjaHJvbWUqDQgAEAAY4wIYsQMYgAQyDQgAEAAY4wIYsQMYgAQyCggBEC4YsQMYgAQyBwgCEAAYgAQyBwgDEAAYgAQyBwgEEAAYgAQyBwgFEC4YgAQyBwgGEAAYgAQyBwgHEAAYgAQyBwgIEAAYgAQyBwgJEAAYgATSAQgyMjgzajBqN6gCALACAA&sourceid=chrome&source=chrome.ob&ie=UTF-8"

# resp = urlopen(url)
# print(resp.status, resp.reason)
# result = unescape(resp.read().decode())
# print(result)

# with open("원빈.html", "w") as f:
#     f.write(unescape(resp.read().decode()))


# url = "https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&q=%EC%9B%90%EB%B9%88"

# resp = urlopen(url)
# print(resp.status, resp.reason)
# result = unescape(resp.read().decode())
# print(result)

# with open("원빈.html", "w") as f:
#     f.write(unescape(resp.read().decode()))


# * 0. robots.txt
# * ----- robotfileparser ------
# * 1. allow, disallow 정책에 의해서 Bot 으로 접근이 가능한지
# * ----- status, code, headers ------
# * 2. google, daum 응답은 정상적으로 오지만 접근 불가
# * naver는 응답, 접근 둘 다 가능
# * response header 에 있는 content-type: boby에 있는 콘텐츠의 형식; text/html; encoding = ?
# * body read => bytes => decode(encoding) + HTML Entities(&#숫자; => unescape)


# * Non ASCII => Hexadecimal => Percent Encoding
from urllib.parse import quote, unquote, urlparse, urlunparse, parse_qs, parse_qsl

# quote("원빈"), unquote("%EC%9B%90%EB%B9%88")

# * netloc/schema => https
# * ://
# * domain => search.daum.net
# * path => /search
# * parameters => key-value (query string)
# * ?w=tot&
# * DA=YZR
# * &t__nil_searchbox=btn
# * &q=%EC%9B%90%EB%B9%88

# url = "https://search.daum.net/search"
# params = {"w": "tot", "DA": "YZR", "t__nil_searchbox": "btn", "q": "%EC%9B%90%EB%B9%88"}

# if params["q"] == quote("원빈"):
#     print("True")

# parse_result = urlparse(
#     "https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&q=%EC%9B%90%EB%B9%88"
# )
# print(f"parse_result: {parse_result}")

# print(f"unparse_result: {urlunparse(parse_result)}")
# print(f"parse_qs: {parse_qs(parse_result[4])}")
# # * parse_qs: {'w': ['tot'], 'DA': ['YZR'], 't__nil_searchbox': ['btn'], 'q': ['원빈']}
# print(f"parse_qsl: {parse_qsl(parse_result[4])}")

# * URL => QueryString 데이터를 담을 수 있음 => ?키1=밸류1&키2=밸류2...
# * 주소 => qs => dict : urlparse
# * => 주소 쪼개고 parse_qs/parse_psl => 분해하고 ~ .. 수정  urlencode => qs 만들고 urlunparse => bytes url 로 만듦

from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode, quote, unquote
from urllib.request import Request, urlopen

# 1. robots.txt
# url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%9B%90%EB%B9%88&ackey=45e960fi"
# parser = RobotFileParser(f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt")
# parser.read()
# print(parser.can_fetch("", urlparse(url).path))

# params = dict(parse_qsl(urlparse(url).query))
# params["query"] = "동궁"
# print(params)

# new_url = urlunparse(urlparse(url)[:4] + (urlencode(params), ""))
# print(new_url)
# resp = urlopen(new_url)
# print(resp.status, resp.reason)

import re

# encoding = re.search("charset=(.+)", resp.headers.get("content-type")).group(1)
# data = resp.read().decode(encoding)

# re.search("<title>(.+)</title>", data).group(1)


def robot(url):
    parser = RobotFileParser(
        f"{urlparse(url).scheme}://{urlparse(url).netloc}/robots.txt"
    )
    parser.read()
    return print(parser.can_fetch("", urlparse(url).path))


# url = "https://httpbin.org/status/"
# robot(url)

from urllib.error import HTTPError

# try:
#     resp = urlopen(url + "500")
#     print("정상")
#     print(resp.status, resp.reason, resp.getheaders())
# except HTTPError as e:
#     print("오류")
#     print(e.status, e.reason, e.getheaders())
#     if 500 <= e.status:
#         print("재시도 해볼만한 요청")
#     else:
#         print("내 잘못. 고쳐야함")

# url = "https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&q=%EC%9B%90%EB%B9%88"

# params = dict(parse_qsl(urlparse(url).query))

# params["q"] = "동궁"
# new_url = urlunparse(urlparse(url)[:4] + (urlencode(params), ""))

# print(new_url)

# # resp = urlopen(new_url)
# # print(resp.status, resp.reason, resp.getheaders())

# headers = {
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
# }


# req = Request(new_url, headers=headers, method="GET")

# # print(req.headers)

# resp = urlopen(req)
# # print(resp.status, resp.reason, resp.getheaders())

# print(unescape(re.search(r"<title>(.+)</title>", resp.read().decode()).group(1)))


url = "https://httpbin.org/"
params = {"a": 1, "b": [1, 2, 3, 4]}

req = Request(url + "get", data=urlencode(params).encode(), method="POST")
# resp = urlopen(req)
# print(resp.status, resp.reason, resp.getheaders())

from json import loads

# print(loads(resp.read()))
# # GET 방식은 body 를 사용하지 않음. 파라미터를 아무리 넘겨도 서버쪽에서는 받지 않음
# req = Request(
#     url + "post?" + urlencode(params), data=urlencode(params).encode(), method="POST"
# )
# print(req.full_url, req.headers, req.data)
# print(loads(urlopen(req).read()))

from requests import request, get, post
from requests.compat import urlparse, urlunparse, quote, unquote, urljoin

# resp = request(method="GET", url=url + "get", params=params)
# print(resp.request.url, resp.request.body)


# # resp.read() == resp.content => bytes
# # resp.read().decode() == resp.text => str
# # json.loads(resp.read()) == resp.json => Python Object

# print(resp.json())

# params["키"] = "밸류"
# resp = request(method="POST", url=url + "post", params=params, data=params)
# print(resp.json())

# 네이버
# url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%9B%90%EB%B9%88&ackey=45e960fi"

# params = dict(parse_qsl(urlparse(url).query))

# resp = get(url=url, params=params)
# print(resp.status_code, resp.reason, resp.headers, resp.request.headers)

# print(re.search("<title>(.+)</title>", resp.text).group(1))

# url = "https://httpbin.org/status/403"
# resp = get(url)
# print(resp.status_code)


# HTTP Status Code 200이 아닐 때, 처리하는 재귀적 함수
from time import sleep


def download(url, params={}, data={}, method="GET", retries=3):
    resp = request(method, url=url, params=params, data=data)
    if 400 <= resp.status_code < 500:  # Client Error
        print(resp.status_code, resp.reason, resp.headers)
        resp = None
    elif 500 <= resp.status_code:  # Server Error
        if retries > 0:
            print("재시도중...")
            sleep(1)
            resp = download(url, params, data, method, retries - 1)

        else:
            print("재시도 횟수 초과")
            print(resp.status_code, resp.reason, resp.headers)
            resp = None

    # try:
    #     resp.raise_for_status()   # 4xx, 5xx면 여기서 HTTPError 발생

    # except HTTPError as e:
    #     if 400 <= resp.status_code < 500:  # Client Error
    #         print(resp.status_code, resp.reason, resp.headers)
    #         resp = None

    #     elif 500 <= resp.status_code:  # Server Error
    #         if retries > 0:
    #             print("재시도중...")
    #             sleep(1)
    #             resp = download(url, params, data, method, retries - 1)
    #         else:
    #             print("재시도 횟수 초과")
    #             print(resp.status_code, resp.reason, resp.headers)
    #             resp = None

    return resp


# download("https://httpbin.org/status/500")


# url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%9B%90%EB%B9%88&ackey=l5d902h7"
# params = dict(parse_qsl(urlparse(url).query))

from requests.compat import urljoin

# print(urljoin(url, "/search.naver"))

# resp = download(url, params=params)
# # print(re.search("<title>(.+)</title>", resp.text).group(1))

# print(resp.text)

from bs4 import BeautifulSoup

# html = """
# <html>
# <head></head>
# <body>
# <div>
# <p>
# <a>go to page</a>
# </p>
# </div>
# </body>
# </html>
# """

# html = """
# <html>
# <head></head>
# <body>
# <div id="result">
# <p class="row">
# <a class="red">go to page1</a>
# <a class="blue">go to page2</a>
# </p>
# </div>
# </body>
# </html>
# """

# dom = BeautifulSoup(html, "html.parser")
# print(type(dom), type(html))

# a = dom.html.body.div.p.a

# print(
#     dom.a.text, dom.text.strip(), re.sub(r"^\s*|\s*S", "", dom.text)
# )  # 공백문자0개 이상으로 시작 | 공백문자 0개 이상으로 끝

# print(dom.find_all("a"))
# print(dom.find(string=re.compile("\d$")))
# print(dom.find_all(name="a", limit=1)[0])


html = html = """
<html>
<head><head>
<div>
    <ul>
        <li>
        <li>
</div>
</LI>
</DiV>
</html>
"""
dom1 = BeautifulSoup(html, "html.parser")  # * 성능 준수함

# print(dom1)
dom2 = BeautifulSoup(html, "lxml")  # * 빠름
# print(dom2)
# print(dom2.li.find_next_sibling())
dom3 = BeautifulSoup(html, "html5lib")  # * 느림
# print(dom3)
# print(dom3.li.find_next_sibling())


from requests import get

resp = get("https://pythonscraping.com/pages/page3.html")
# print(resp.status_code, resp.reason)
# print(resp.headers["content-type"])

# resp.text => charset decoding str 객체
# resp.content => bytes 객체

dom = BeautifulSoup(resp.content, "html.parser")

# print(dom.find(attrs={"id": "footer"}))

# print(
#     [tag.name for tag in dom.div.find_all(recursive=False)]
# )  # recursive : 자식만 찾겠다

# html.parser/lxml
# document
# HTML
# HEAD            BODY
# DIV
# IMG H1 #DIV #TABLE #DIV

dom2 = BeautifulSoup(resp.content, "html5lib")
# print([tag.name for tag in dom2.head.find_all(recursive=False)])

# html5lib
# document
# HTML
# HEAD            BODY
# DIV
# IMG H1 #DIV #TABLE #P #DIV

footer = dom2.find(attrs={"id": "footer"})
# ... table    p      footer
#     앞에[-1]   앞에[0]
# find_previous_siblings()는 결과를 "가까운 순서(역순)"로 리스트에 담아주기 때문에,
# 문서상 더 앞쪽(더 먼)에 있는 태그를 가져오려면 [0]이 아니라 [-1]을 써야 한다.
# print(footer.find_previous_siblings(limit=2)[-1])
# print(footer.find_parent().find_all(name="table", recursive=False))
# print(footer.find_parent("body").find(attrs={"id": "giftList"}))

# print(
#     footer.find_parent()
#     .find(name="table")
#     .find()
#     .find_all(recursive=False)[-1]
#     .find_all(recursive=False)[-2]
#     .text.strip()
# )

# print(dom.find_all("td")[-2].text)

# print(dom.find(string=re.compile("1.50")).find_parent().text.strip())

# print(dom.find_all("img")[1:])
# print(dom.find_all(name="img", attrs={"src": re.compile("[1-6][.]jpg$")}))

# for td in dom.find_all("td"):
#     if td.find("img") != None:
#         print(td.find("img"))
data = []
for tr in dom.find_all(name="tr"):
    if len(tr.find_all("td", recursive=False)) > 0:  # th 걸러내기 위해
        td = tr.find_all("td", recursive=False)[2]
        data.append(td.text.strip())


# print(data)


imgs = []
for tr in dom.find_all(name="tr"):
    if len(tr.find_all("td", recursive=False)) > 0:  # th 걸러내기 위해
        td = tr.find_all("td", recursive=False)[3]
        imgs.append(td.img.attrs["src"])


# print(imgs)


from requests.compat import urljoin

# print([urljoin(resp.request.url, src) for src in imgs])


resp = get("https://pythonscraping.com/img/gifts/img4.jpg")
# print(resp.status_code, resp.reason, resp.headers)


# print(re.search(r"/(img[1-6])\.jpg$", resp.request.url).group(1))
# print(re.search(r"image/(jpg|jpeg|bmp|png)", resp.headers["content-type"]).group(1))


# * 파일 저장
with open("img4.jpeg", "wb") as fp:
    fp.write(resp.content)


from urllib.parse import parse_qsl

url = "https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&q=%EC%9B%90%EB%B9%88"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
}

params = dict(parse_qsl(re.search(r"[?](.+)$", url).group(1)))

url = re.search(r"^(.+)[?]", url).group(1)
# req = Request(new_url, headers=headers, method="GET")
resp = get(url=url, params=params, headers=headers)
# print(resp.status_code, resp.reason, resp.headers["content-type"])

dom = BeautifulSoup(resp.text, "html5lib")

# print(dom.title)

# print(len(dom.find_all("c-doc-web")))

# for row in dom.find_all("c-doc-web"):
#     print(row.find("c-title").text.strip())
#     print(row.find("c-title").attrs["data-href"])


# print(dom.find(name="div", attrs={"id": "fdr-d1a052bd423a40f79324d68b64175dfa"}))
# result = dom.find_all(name="div", attrs={"id": re.compile(r"^fdr-")})[0]
# for row in result.find().find().find().find_all(name="div", recursive=False):
#     link = row.find().find_all(recursive=False)[0]
#     desc = row.find().find_all(recursive=False)[1]
#     print(link.a.attrs["href"])
#     print(desc.find(name="span").text.strip())


# * find => DOM 트리에서 특정 한 노드에서의 관계만 갖고 탐색
# * tag name      => find계열의 함수들에서 name 에 해당되는 부분
# * # id          => find계열의 함수들에서 attrs={'id':?} 에 해당되는 부분
# * # .class      => find계열의 함수들에서 attrs={'class':?} 에 해당되는 부분
# * # c-item      => find계열의 함수들에서 attrs={'c-item':?} 에 해당되는 부분

# * div     #id => 자손
# * div >   #id => 자식(>)

# * div:has(> a) => find('a').find_parent('div')
# * 대상: div, 조건: a가 자식인 애

# * div:has(+ a) => find('a').find_previous_sibling()
# * 대상: div, 조건: 내 다음 형제가 a인 애

resp = get("https://pythonscraping.com/pages/page3.html")
dom = BeautifulSoup(resp.text, "html.parser")

print([td.text.strip() for td in dom.select("table tr > td:nth-child(3)")])

print([td.attrs["src"] for td in dom.select("table tr > td:nth-child(4) > img")])

print(dom.select("table *[src$=jpg]"))
