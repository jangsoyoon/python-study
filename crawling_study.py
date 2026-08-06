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

parser = RobotFileParser()

parser.set_url("https://www.korea.ac.kr/robots.txt")

parser.read()
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


url = "https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&q=%EC%9B%90%EB%B9%88"

resp = urlopen(url)
print(resp.status, resp.reason)
result = unescape(resp.read().decode())
print(result)

with open("원빈.html", "w") as f:
    f.write(unescape(resp.read().decode()))


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

url = "https://search.daum.net/search"
params = {"w": "tot", "DA": "YZR", "t__nil_searchbox": "btn", "q": "%EC%9B%90%EB%B9%88"}

if params["q"] == quote("원빈"):
    print("True")

parse_result = urlparse(
    "https://search.daum.net/search?w=tot&DA=YZR&t__nil_searchbox=btn&q=%EC%9B%90%EB%B9%88"
)
print(f"parse_result: {parse_result}")

print(f"unparse_result: {urlunparse(parse_result)}")
print(f"parse_qs: {parse_qs(parse_result[4])}")
# * parse_qs: {'w': ['tot'], 'DA': ['YZR'], 't__nil_searchbox': ['btn'], 'q': ['원빈']}
print(f"parse_qsl: {parse_qsl(parse_result[4])}")

# * URL => QueryString 데이터를 담을 수 있음 => ?키1=밸류1&키2=밸류2...
# * 주소 => qs => dict : urlparse
# * => 주소 쪼개고 parse_qs/parse_psl => 분해하고 ~ .. 수정  urlencode => qs 만들고 urlunparse => bytes url 로 만듦
