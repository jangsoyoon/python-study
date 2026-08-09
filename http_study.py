from hmac import new
import json
from re import ASCII, L
from urllib.request import Request, urlopen

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


url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%9B%90%EB%B9%88&ackey=l5d902h7"
params = dict(parse_qsl(urlparse(url).query))

from requests.compat import urljoin

print(urljoin(url, "/search.naver"))

resp = download(url, params=params)
# print(re.search("<title>(.+)</title>", resp.text).group(1))

print(resp.text)
