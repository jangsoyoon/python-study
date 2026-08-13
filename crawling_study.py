import html
from os import mkdir
import xml

import attr
from requests import request
from requests.compat import urljoin, urlparse
from bs4 import CSS, BeautifulSoup
import re
import sqlite3

# DBMS => 데이터 저장/관리/검색
# Crawler => 데이터 수집

# URL Pool => URL => Bot/Spider/Crawler => URL List
#           전략: 탐색공간 - BFS(Queue), DFS(Stack)
# FocusedCrawling - 휴리스틱 전략(Depth, Domain, Tag 제한)
#     Req => Resp => Text/HTML => DOM => HyperLinks
#                                      이미 방문한 적이 있는지? => 전략
#                                      없으면 URL List
import sqlite3

con = sqlite3.connect("robots.db")
# cur = con.cursor()

# url = "https://google.com/robots.txt"
# resp = request(url=url, method="GET")
# # print(resp.text[:100])
# re.findall(r"^Disallow:\s*(.+)$", resp.text, re.IGNORECASE | re.MULTILINE)

# #  HOST                 DISALLOW
# # PK domain         PK FK path => disallow
# # 1  google.com     1  1  /search
# cur.executescript("""
#     CREATE TABLE IF NOT EXISTS HOST(
#         PK INTEGER PRIMARY KEY,
#         DOMAIN TEXT NOT NULL
#     );
#     CREATE TABLE IF NOT EXISTS DISALLOW(
#         PK INTEGER PRIMARY KEY,
#         FK INTEGER NOT NULL,
#         PATH TEXT NOT NULL
#     );
# """)
# url = "https://www.google.com/search?q=어쩌고"
# urlparse(url).netloc, urlparse(url).path
# urljoin(url, "/robots.txt")

# robots_url = urljoin(url, "/robots.txt")
# resp = request(url=robots_url, method="GET")
# if resp.status_code != 200:
#     "통과"
# else:
#     paths = re.findall(r"^Disallow:\s*(.+)$", resp.text, re.IGNORECASE | re.MULTILINE)
# cur.execute("INSERT INTO HOST(DOMAIN) VALUES(?)", [urlparse(url).netloc])
# FK = cur.lastrowid
# cur.executemany(
#     "INSERT INTO DISALLOW(FK, PATH) VALUES(?,?)", [(FK, path) for path in paths]
# )

# con.commit()
# con.close()
# with sqlite3.connect("robots.db") as con:
#     cur = con.cursor()
#     cur.execute("SELECT PK FROM HOST WHERE DOMAIN=?", [urlparse(url).netloc])
#     FK = cur.fetchone()
#     if FK is None:
#         "새롭게 robots.txt 추가해야함"

#     cur.execute("SELECT PK FROM HOST WHERE DOMAIN=?", [urlparse(url).netloc])
#     FK = cur.fetchone()[0]
#     cur.execute("SELECT PATH FROM DISALLOW WHERE FK=?", [FK])
#     disallow_list = [
#         re.compile(re.escape(row[0]))  # re.compile(r'^'+re.escape(row[0])+r'$')
#         for row in cur.fetchall()
#     ]

#     print(
#         sum(
#             map(
#                 lambda p: 0 if p.search(urlparse(url).path) is None else 1,
#                 disallow_list,
#             )
#         )
#     )


# robots.txt 검사
def canFetch(url):
    # 리턴값
    result = True
    components = urlparse(url)

    # robots.txt 있으면,
    if resp.status_code == 200:
        paths = re.findall(
            r"^Disallow:\s*(.+)$", resp.text, re.IGNORECASE | re.MULTILINE
        )

        with sqlite3.connect("robots.db") as con:
            cur = con.cursor()
            cur.execute("SELECT PK FROM HOST WHERE DOMAIN=?", [components.netloc])
            FK = cur.fetchone()

            # 전에 저장된 robots.txt가 있으면,
            if FK is None:
                cur.execute("INSERT INTO HOST(DOMAIN) VALUES(?)", [components.netloc])
                FK = cur.lastrowid
                cur.executemany(
                    "INSERT INTO DISALLOW(FK, PATH) VALUES(?,?)",
                    [(FK, path) for path in paths],
                )
                con.commit()

            cur.execute("SELECT PK FROM HOST WHERE DOMAIN=?", [components.netloc])
            FK = cur.fetchone()[0]
            cur.execute("SELECT PATH FROM DISALLOW WHERE FK=?", [FK])
            disallow_list = [
                re.compile(re.escape(row[0]))  # re.compile(r'^'+re.escape(row[0])+r'$')
                for row in cur.fetchall()
            ]

            s = sum(
                map(
                    lambda p: 0 if p.search(urlparse(url).path) is None else 1,
                    disallow_list,
                )
            )
            result = False if s > 0 else True
    return result


# URLs = list()
# URLs.append(
#     (
#         1,
#         "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%9B%90%EB%B9%88&ackey=4djr57o6",
#     )
# )

# # Focused Crawling
# # 1. Depth 제한 = 2
# DEPTH = 5

# # 방문한적 있는지 체크하는 URL-seen
# seen = list()
# WHITELIST = ["blog.naver.com"]  # 여기에 있는 도메인만 방문해
# BLACKLIST = ["www.navercorp.com"]  # 여기에 있는 도메인은 방문하지마

# # URL Pool에 더이상 URL이 없을때까지
# while URLs:
#     # Starting URL
#     depth, url = URLs.pop(
#         0
#     )  # BFS, Queue // 맨 앞(가장 오래된 것)을 꺼냄 -> FIFO -> BFS
#     # depth, url = = URLs.pop(-1)   # 맨 뒤(가장 최근 것)를 꺼냄 -> LIFO -> DFS
#     # 방문한 적 있는 url => seen에 추가
#     seen.append((depth, url))

#     # 1. Depth 검사
#     if depth > DEPTH:
#         continue

#     # 2. Domain 검사 - seen 에는 추가되지만, 실제 방문은 X
#     if urlparse(url).netloc in BLACKLIST and urlparse(url).netloc not in WHITELIST:
#         continue

#     # Request-Response
#     # sleep(1) => 너무 많은 트래픽 X
#     resp = request(url=url, method="GET")
#     if resp.status_code != 200:
#         if resp.status_code >= 500:
#             URLs.append(url)  # 500 Server Error 재시도
#         else:
#             continue  # 다음 URL로 넘길때

#     # Response.body => DOM 변환
#     if re.search("text/html", resp.headers.get("content-type", "")):
#         dom = BeautifulSoup(resp.text, "html.parser")
#         # HyperLink 추출
#         links = dom.select("a[href]")
#         # URL Normalization
#         for link in links:
#             nurl = urljoin(url, link.attrs["href"])
#             # http 로 시작하지 않으면 skip
#             if re.match("http", nurl) is None or re.match("#", link.attrs["href"]):
#                 continue
#             # 방문한 적이 없으면 + 앞으로 방문할 예정 목록에도 없으면
#             if nurl not in [row[1] for row in seen] and nurl not in [
#                 row[1] for row in URLs
#             ]:
#                 URLs.append((depth + 1, nurl))
#     # print(f"len(seen), len(URLs): {len(seen), len(URLs)}")
#     print(seen)


# URLs = list()
# URLs.append((1, "https://news.naver.com"))

# # Focused Crawling
# # 1. Depth 제한 = 2
# DEPTH = 5

# # 방문한적 있는지 체크하는 URL-seen
# seen = list()
# WHITELIST = ["news.naver.com", "n.news.naver.com"]  # 여기에 있는 도메인만 방문해
# BLACKLIST = [""]  # 여기에 있는 도메인은 방문하지마

# URL Pool에 더이상 URL이 없을때까지
# while URLs:
#     # Starting URL
#     depth, url = URLs.pop(
#         0
#     )  # BFS, Queue // 맨 앞(가장 오래된 것)을 꺼냄 -> FIFO -> BFS
#     # depth, url = = URLs.pop(-1)   # 맨 뒤(가장 최근 것)를 꺼냄 -> LIFO -> DFS
#     # 방문한 적 있는 url => seen에 추가
#     seen.append((depth, url))

#     # 1. Depth 검사
#     if depth > DEPTH:
#         continue

#     # 2. Domain 검사 - seen 에는 추가되지만, 실제 방문은 X
#     if urlparse(url).netloc in BLACKLIST and urlparse(url).netloc not in WHITELIST:
#         continue

#     # 3. 영역 제한 => 페이지 내 (Element.Tag.name)

#     # Request-Response
#     # sleep(1) => 너무 많은 트래픽 X
#     resp = request(url=url, method="GET")
#     if resp.status_code != 200:
#         if resp.status_code >= 500:
#             URLs.append(url)  # 500 Server Error 재시도
#         else:
#             continue  # 다음 URL로 넘길때

#     # Response.body => DOM 변환
#     if re.search("text/html", resp.headers.get("content-type", "")):
#         dom = BeautifulSoup(resp.text, "html.parser")
#         # 3. 영역제한
#         # 3.1 메뉴제한
#         # for li in dom.find(attrs={'class':'Nlnb_menu_list'}).find_all('li'):
#         # li.find('a').attrs['href']
#         links = []
#         if dom.select_one("ul.Nlnb_menu_list"):
#             links.extend(dom.select(".Nlnb_menu_list > li > a[href]"))

#         # 3.2 헤드라인제한
#         if dom.select_one(".section_article"):
#             links.extend(dom.select("a.sa_text_title[href]"))

#         # 3.3 본문제한
#         if dom.select_one("#contents"):
#             title = dom.select_one("h2#title_area")
#             content = dom.select_one("article#dic_area")
#             with open(
#                 r"./news/" + re.search(r"(\d{8,})$", url).group(1) + ".txt", "w"
#             ) as fp:
#                 fp.write(title.text.strip())
#                 fp.write("\n\n\n\n\n")
#                 fp.write(content.text.strip())

#         # URL Normalization
#         for link in links:
#             nurl = urljoin(url, link.attrs["href"])
#             # http 로 시작하지 않으면 skip
#             if re.match("http", nurl) is None or re.match("#", link.attrs["href"]):
#                 continue

#             # 방문한 적이 없으면 + 앞으로 방문할 예정 목록에도 없으면
#             if nurl not in [row[1] for row in seen] and nurl not in [
#                 row[1] for row in URLs
#             ]:
#                 URLs.append((depth + 1, nurl))
#     # print(f"len(seen), len(URLs): {len(seen), len(URLs)}")
#     print(seen)


# url = "https://news.naver.com/section/100"

# dom = BeautifulSoup(request(url=url, method="GET").text, "html.parser")
# print(urljoin(url, [a.attrs["href"] for a in dom.select("a.sa_text_title[href]")]))
# urljoin(url, [a.attrs['href'] for a in dom.select("a.sa_text_title[href]")])

# con = sqlite3.connect("news.db")
# cur = con.cursor()

# cur.executescript("""
#                   CREATE TABLE IF NOT EXISTS LINK(
#                       PK INTEGER PRIMARY KEY,
#                       DEPTH INTEGER NOT NULL DEFAULT 1,
#                       REFERRER TEXT NOT NULL DEFAULT '',
#                       URL TEXT NOT NULL,
#                       REDGATE DATETIME DEFAULT CURRENT_TIMESTAMP
#                   );

#                   CREATE TABLE IF NOT EXISTS NEWS(
#                       PK INTEGER PRIMARY KEY,
#                       FK INTEGER NOT NULL,
#                       TITLE TEXT NOT NULL,
#                       CONTENT TEXT NOT NULL,
#                       REDGATE DATETIME DEFAULT CURRENT_TIMESTAMP
#                   );
#                   """)
# con.commit()


# URLs = list()
# URLs.append((1, "", "https://news.naver.com"))

# # Focused Crawling
# # 1. Depth 제한 = 2
# DEPTH = 5

# # 방문한적 있는지 체크하는 URL-seen
# seen = list()
# WHITELIST = ["news.naver.com", "n.news.naver.com"]  # 여기에 있는 도메인만 방문해
# BLACKLIST = [""]  # 여기에 있는 도메인은 방문하지마

# # URL Pool에 더이상 URL이 없을때까지
# while URLs:
#     # Starting URL
#     # print("현재 큐 앞부분:", URLs[:3])
#     depth, referrer, url = URLs.pop(
#         0
#     )  # BFS, Queue // 맨 앞(가장 오래된 것)을 꺼냄 -> FIFO -> BFS
#     # depth, url = = URLs.pop(-1)   # 맨 뒤(가장 최근 것)를 꺼냄 -> LIFO -> DFS
#     # 방문한 적 있는 url => seen에 추가
#     seen.append((depth, referrer, url))

#     # 1. Depth 검사
#     if depth > DEPTH:
#         continue

#     # 2. Domain 검사 - seen 에는 추가되지만, 실제 방문은 X
#     if urlparse(url).netloc in BLACKLIST and urlparse(url).netloc not in WHITELIST:
#         continue

#     # 3. 영역 제한 => 페이지 내 (Element.Tag.name)

#     # Request-Response
#     # sleep(1) => 너무 많은 트래픽 X
#     resp = request(url=url, method="GET")
#     if resp.status_code != 200:
#         if resp.status_code >= 500:
#             URLs.append((depth, referrer, url))  # 500 Server Error 재시도
#         else:
#             continue  # 다음 URL로 넘길때

#     # Response.body => DOM 변환
#     if re.search("text/html", resp.headers.get("content-type", "")):
#         dom = BeautifulSoup(resp.text, "html.parser")
#         with sqlite3.connect("news.db") as con:
#             cur = con.cursor()
#             cur.execute(
#                 """
#                         select * from link where url = ?
#                         """,
#                 [url],
#             )
#             if len(cur.fetchall()) == 0:
#                 cur.execute(
#                     """
#                             insert into link(depth, referrer, url) values
#                             (?, ?, ?)
#                             """,
#                     [depth, referrer, url],
#                 )
#                 con.commit()

#         # 3. 영역제한
#         # 3.1 메뉴제한
#         # for li in dom.find(attrs={'class':'Nlnb_menu_list'}).find_all('li'):
#         # li.find('a').attrs['href']
#         links = []
#         if dom.select_one("ul.Nlnb_menu_list"):
#             links.extend(dom.select(".Nlnb_menu_list > li > a[href]"))

#         # 3.2 헤드라인제한
#         if dom.select_one(".section_article"):
#             links.extend(dom.select("a.sa_text_title[href]"))

#         # 3.3 본문제한
#         if dom.select_one("#contents"):
#             title = dom.select_one("h2#title_area")
#             content = dom.select_one("article#dic_area")
#             # with open(
#             #     r"./news/" + re.search(r"(\d{8,})$", url).group(1) + ".txt", "w"
#             # ) as fp:
#             #     fp.write(title.text.strip())
#             #     fp.write("\n\n\n\n\n")
#             #     fp.write(content.text.strip())

#             with sqlite3.connect("news.db") as con:
#                 cur = con.cursor()
#                 cur.execute(
#                     """
#                             insert into news(fk, title, content)
#                             values ((select pk from link where url = ? limit 0, 1), ?, ?)
#                             """,
#                     [url, title.text.strip(), content.text.strip()],
#                 )
#                 con.commit()

#         # URL Normalization
#         for link in links:
#             nurl = urljoin(url, link.attrs["href"])
#             # http 로 시작하지 않으면 skip
#             if re.match("http", nurl) is None or re.match("#", link.attrs["href"]):
#                 continue

#             # 방문한 적이 없으면 + 앞으로 방문할 예정 목록에도 없으면
#             if nurl not in [row[1] for row in seen] and nurl not in [
#                 row[1] for row in URLs
#             ]:
#                 URLs.append((depth + 1, url, nurl))

# con.close()
# print(f"len(seen), len(URLs): {len(seen), len(URLs)}")
# print(seen)
# ext = {
#     "javascript": "js",
#     "css": "css",
#     "html": "html",
#     "jpeg": "jpg",
#     "jpg": "jpg",
#     "png": "png",
#     "bmp": "bmp",
# }

# URLs = list()
# URLs.append(
#     "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%9B%90%EB%B9%88&ackey=4djr57o6"
# )

# seen = list()

# while URLs:
#     url = URLs.pop(0)
#     seen.append(url)

#     resp = request(url=url, method="GET")
#     if resp.status_code != 200:
#         if resp.status_code >= 500:
#             URLs.append(url)
#         else:
#             continue

#     fname = re.sub(r"[$?!#]", "", re.search(r".+[/]([^/]+)$", url).group(1))

#     if re.search("text", resp.headers["content-type"]):
#         fext = ext.get(
#             re.search(r"text/(\w+)", resp.headers["content-type"]).group(1), "txt"
#         )
#         with open(f"./dummy/{fname}.{fext}", "w") as fp:
#             fp.write(resp.text)

#         if re.search("text/html", resp.headers["content-type"]):
#             dom = BeautifulSoup(resp.text, "html.parser")
#             links = dom.select("script[src], img[src], link[href]")

#             for link in links:
#                 nurl = urljoin(
#                     url,
#                     link.attrs["src"] if link.has_attr("src") else link.attrs["href"],
#                 )
#                 if re.match("http", nurl) is None or re.match(
#                     "#",
#                     link.attrs["src"] if link.has_attr("src") else link.attrs["href"],
#                 ):
#                     continue

#                 if nurl not in seen and nurl not in URLs:
#                     URLs.append(nurl)
#     # if re.search('application', resp.headers['content-type']):
#     if re.search("image", resp.headers["content-type"]):
#         fext = ext.get(
#             re.search(r"image/(\w+)", resp.headers["content-type"]).group(1), "txt"
#         )
#         with open(f"./dummy/{fname[:20]}.{fext}", "wb") as fp:
#             fp.write(resp.content)
