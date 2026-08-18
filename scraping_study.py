from operator import itemgetter


from grpc import Server
from mdurl import URL
from requests import get
from bs4 import BeautifulSoup

#######################! scraping#######################
# url = "https://www.ppomppu.co.kr/zboard/view.php?id=money&page=1&divpage=98&no=546862"
# resp = get(url)

# print(resp.status_code, resp.headers["content-type"])

# dom1 = BeautifulSoup(resp.text, "html.parser")
# dom2 = BeautifulSoup(resp.text, "lxml")
# dom3 = BeautifulSoup(resp.text, "html5lib")

# print(len(dom1.select(".board-contents")))
# print(len(dom2.select(".board-contents")))
# print(len(dom3.select(".board-contents")))
path = "table table table tr:first-child > td"
# print((dom1.select_one(path).text.strip()))
# print((dom2.select_one(path).text.strip()))
# print((dom3.select_one(path).text.strip()))
# print(resp.text)


# url = "https://pythonscraping.com/pages/javascript/ajaxDemo.html"
# resp = get(url)
# dom = BeautifulSoup(resp.text, "html.parser")
# # print(dom.select_one("body script"))

# url = "https://pythonscraping.com/pages/javascript/loadedContent.php"
# # print(BeautifulSoup(get(url).text, "html.parser").text.strip())


# url = "https://comic.naver.com/index"
# resp = get(url)
# dom = BeautifulSoup(resp.text, "html.parser")

# * Client ---------------> Req ----------------> Server
# *     DOM  <-----------   HTML   -----------
# *          ------------> XHR-Req ----------->
# *    갱신  <-----------   DATA   -----------


# url = "https://brunch.co.kr"
# resp = get(url)
# dom = BeautifulSoup(resp.text, "html.parser")
# print(dom.form.attrs["action"], dom.form.attrs["method"])


# for tag in dom.form.select("input"):
#     print(tag.attrs["name"], tag.attrs["value"] if tag.has_attr("value") else None)


# url = "https://brunch.co.kr/search?q=원빈"
# resp = get(url)
# dom = BeautifulSoup(resp.text, "html.parser")

# print(dom.select("#resultArticle"))
import re
import json
from urllib.parse import parse_qsl

url = "http://api.brunch.co.kr/v1/search/article?q=%EC%9B%90%EB%B9%88&page=1&pageSize=20&highlighter=y&escape=y&sortBy=accu"
url, params = re.split(r"\?", url)
params = dict(parse_qsl(params))


params["highlighter"] = "n"
resp = get(url, params=params)
# print(resp.status_code, resp.headers["content-type"])
# print(url, params)


# for item in resp.json()["data"]["list"]:
#     print(item["title"])


# 네이버 자동완성 가져오기

url = "https://ac.search.naver.com/nx/ac?q=%EC%9B%90&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100&ackey=jmkx8d6q&_callback=_jsonp_4"
url, params = url.split("?")
# print(dict(parse_qsl(params)))
params = dict(parse_qsl(params)[:-2])
# print(url, params)

# resp = get(url, params=params)


# print(",".join([item[0] for item in resp.json()["items"][0]]))


# while True:
#     q = input()
#     if q == "q":
#         break

#     params["q"] = q
#     resp = get(url, params)
#     print(",".join([item[0] for item in resp.json()["items"][0]]))


url = "https://suggest-api-ext.onkakao.net/tot-pc/search?q=%E3%85%87%E3%85%8F%E3%84%B4"
url, params = url.split("?")
params = dict(parse_qsl(params))
# print(url, params)

resp = get(url, params=params)

# print([item["keyword"] for item in resp.json()["subkeys"]])

# for item in resp.json()["subkeys"]:
#     print(item["keyword"])

# while True:
#     q = input()
#     if q == "q":
#         break

#     params["q"] = q
#     resp = get(url, params)

#     print(",".join([item["keyword"] for item in resp.json()["subkeys"]]))

page_no = 0
# url = "https://www.scrapingcourse.com/pagination/"
# for page_no in range(1, 20):

#     new_url = url + str(page_no)
#     resp = get(new_url)
#     if resp.status_code != 200:
#         print(page_no)
#         continue

#     if re.search("text/html", resp.headers["content-type"]):
#         dom = BeautifulSoup(resp.text, "html.parser")
#         print([[item.text.strip()] for item in dom.select(".product-name")])


url = "https://www.scrapingcourse.com/ajax/products"
offset = 0

# while True:
#     print(offset)
#     new_url = url + str(f"?offset={offset}")
#     resp = get(new_url)
#     if resp.status_code != 200:
#         break

#     if re.search("text/html", resp.headers["content-type"]):
#         dom = BeautifulSoup(resp.text, "html.parser")
#         items = dom.select(".product-name")

#         if not items:
#             print("더 이상 데이터가 없음")
#             break

#         print([[item.text.strip()] for item in items])
#         offset += 10


# 웹툰
# # 1. 웹툰 목록 => titleId 확인

# XHR: https://comic.naver.com/api/home/component?type=DAILY_WEBTOON&order=VIEW
# # 2. 어떤 웹툰의 회차 목록 => titleId 웹툰에서의 회차 no 확인
# https://comic.naver.com/webtoon/list?titleId=828402&page=1&sort=DESC
# XHR: https://comic.naver.com/api/article/list?titleId=828402&page=1&sort=DESC
# # 3. 어떤 웹툰의 특정 회차의 내용 => titleId&no
# https://comic.naver.com/webtoon/detail?titleId=828402&no=87&week=tue


url = "https://comic.naver.com/api/home/component?type=DAILY_WEBTOON&order=VIEW"
resp = get(url)
# if resp.status_code == 200 and re.search("json", resp.headers["content-type"]) != None:
#     webtoon_list = [
#         (item["titleId"], item["titleName"]) for item in resp.json()["titleList"]
#     ]
#     url = f"https://comic.naver.com/api/article/list?titleId={webtoon_list[1][0]}&page=1&sort=DESC"
#     resp = get(url)
#     if (
#         resp.status_code == 200
#         and re.search("json", resp.headers["content-type"]) != None
#     ):
#         no_list = [
#             (item["no"], item["subtitle"]) for item in resp.json()["articleList"]
#         ]
#         url = f"https://comic.naver.com/webtoon/detail?titleId={webtoon_list[1][0]}&no={no_list[0][0]}"
#         resp = get(url)
#         if (
#             resp.status_code == 200
#             and re.search("html", resp.headers["content-type"]) != None
#         ):
#             dom = BeautifulSoup(resp.text, "html.parser")
#             print(
#                 [img.attrs["src"] for img in dom.select("#sectionContWide img[src]")][
#                     :5
#                 ]
#             )
import sqlite3

with sqlite3.connect("naver_webtoon.db") as con:
    cur = con.cursor()
    # cur.executescript("""
    #                   CREATE TABLE IF NOT EXISTS WEBTOON_LIST(
    #                       PK INTEGER PRIMARY KEY,
    #                       TITLEID INTEGER NOT NULL,
    #                       TITLENAME TEXT NOT NULL
    #                       );

    #                   CREATE TABLE IF NOT EXISTS NO_LIST(
    #                       PK INTEGER PRIMARY KEY,
    #                       FK INTEGER NOT NULL,
    #                       NO INTEGER NOT NULL,
    #                       SUBTITLE TEXT NOT NULL
    #                                               );
    #                  CREATE TABLE IF NOT EXISTS IMG_LIST(
    #                     PK INTEGER PRIMARY KEY,
    #                     FK INTEGER NOT NULL,
    #                     URL TEXT NOT NULL,
    #                     PATH TEXT NOT NULL,
    #                     FLAG TEXT NOT NULL DEFAULT 'N',
    #                     REGDATE DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    #                                           );
    #                   """)
    from requests.compat import urljoin

    URLs = []
    Seen = []

    URLs.append(
        "https://comic.naver.com/api/home/component?type=DAILY_WEBTOON&order=VIEW"
    )

    while URLs:
        url = URLs.pop(0)
        # 갔다 왔다는 것을 보려고
        Seen.append(url)
        resp = get(url)

        if resp.status_code != 200:
            print(resp.status_code, url)
            continue

        if re.search("application/json", resp.headers["content-type"]):
            data = resp.json()
            if "titleList" in data.keys():  # 웹툰 목록
                with sqlite3.connect("naver_webtoon.db") as con:
                    cur = con.cursor()
                    for item in data["titleList"][:2]:
                        cur.execute(
                            """
                                            select * from WEBTOON_LIST where titleId=?
                                            """,
                            [item["titleId"]],
                        )
                        # 웹툰 목록에 있는 각 웹툰들이 DB에 있는지 확인, 만약에 없으면 추가
                        if cur.fetchone() is None:
                            cur.execute(
                                """
                                                insert into WEBTOON_LIST(titleId, titleName) values(?,?)
                                                """,
                                [item["titleId"], item["titleName"]],
                            )
                        # Crawler => HTML => Link Extraction => Normalized NewURL => URL Pool
                        new_url = f"https://comic.naver.com/api/article/list?titleId={item['titleId']}&page=1&sort=DESC"
                        if (
                            new_url not in Seen and new_url not in URLs
                        ):  # 특정 웹툰의 회차목록 URI
                            URLs.append(new_url)
                    con.commit()
            if "articleList" in data.keys():  # 회차 목록
                with sqlite3.connect("naver_webtoon.db") as con:
                    # 어떤 웹툰인지는 모르고 오로지 회차 목록을 불러오는 곳
                    cur = con.cursor()
                    titleId = dict(parse_qsl(url.split("?")[1]))["titleId"]
                    cur.execute(
                        """
                                select pk from WEBTOON_LIST where titleId = ?
                                """,
                        [titleId],
                    )

                    FK = cur.fetchone()[0]
                    for item in data["articleList"][:1]:
                        cur.execute(
                            """
                                        select * from NO_LIST where no=?
                                        """,
                            [item["no"]],
                        )
                        if cur.fetchone() is None:
                            cur.execute(
                                """
                                            insert into NO_LIST(fk, no, subtitle) values(?,?,?)
                                            """,
                                [FK, item["no"], item["subtitle"]],
                            )
                        new_url = url = (
                            "https://comic.naver.com/webtoon/detail?titleId={}&no={}".format(
                                titleId, item["no"]
                            )
                        )
                        if new_url not in Seen and new_url not in URLs:
                            URLs.append(new_url)
                    con.commit()
        if re.search("text/html", resp.headers["content-type"]):
            dom = BeautifulSoup(resp.text, "html.parser")
            params = dict(parse_qsl(url.split("?")[1]))
            titleId = params["titleId"]
            no = params["no"]
            # 이미지 찾고

            with sqlite3.connect("naver_webtoon.db") as con:
                # 어떤 웹툰인지는 모르고 오로지 회차 목록을 불러오는 곳
                cur = con.cursor()
                cur.execute(
                    """
                            select pk from no_list where fk = (
                                select pk from webtoon_list where titleId = ? limit 0,1
                            ) and no = ?
                            """,
                    [titleId, no],
                )
                FK = cur.fetchone()[0]
                for img in dom.select("#sectionContWide > img[src]"):
                    new_url = urljoin(url, img.attrs["src"])
                    cur.execute(
                        """
                                select * from img_list where fk = ? and url = ?
                                """,
                        [FK, new_url],
                    )

                    if cur.fetchone() is None:
                        cur.execute(
                            """
                                        insert into img_list(fk, url, path) values(?,?,"")
                                        """,
                            [FK, new_url],
                        )

                    if new_url not in Seen and new_url not in URLs:
                        URLs.append(new_url)
                con.commit()
        # if re.search("image", resp.headers["content-type"]):
        #     # 이미지 저장 => PATH, FLAG 업데이트
        #     for img in dom.select("#sectionContWide > img[src]"):
        #         no = params["no"]
        #         new_url = urljoin(url, img.attrs["src"])
        #         cur.execute(
        #             """
        #                     select pk from img_list where fk =
        #                     (select * from no_list where pk = ?) and url = ?
        #                     """,
        #             [no, new_url],
        #         )
        #         PK = cur.fetchone()
        #         if cur.fetchone() is None:
        #             cur.execute(
        #                 """
        #                             update IMG_LIST set path = '' and flag = '' where pk = ?
        #                             """,
        #                 [PK],
        #             )

        #         if new_url not in Seen and new_url not in URLs:
        #             URLs.append(new_url)
        #     con.commit()


con = sqlite3.connect("naver_webtoon.db")
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
}

cur = con.cursor()

while True:
    cur.execute("""
                select pk, url from img_list where flag == 'N' order by regdate asc limit 0, 10
                """)
    URLs = cur.fetchall()

    # 더 이상 수집할 이미지가 없을 때,
    if len(URLs) == 0:
        break

    while URLs:
        pk, url = URLs.pop(0)

        resp = get(url, headers=headers)

        if resp.status_code != 200:
            continue

        if re.search("image", resp.headers["content-type"]):
            fname = re.search(r".+/(.+)$", url).group(1)
            with open(f"webtoon/{fname}", "wb") as fp:
                fp.write(resp.content)
                cur.execute(
                    """
                            update img_list set flag = 'Y', path = ?, regdate = CURRENT_TIMESTAMP where pk = ?
                            """,
                    [f"webtoon/{fname}", pk],
                )

                con.commit()
    break
con.close()
