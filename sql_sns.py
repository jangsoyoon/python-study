# content = 본문내용
# tags = 사용자가 달려고 하는 해시태그들
# 리턴: 성공시 id, 실패시 None

import sqlite3

con = sqlite3.connect("sns.db")  # Create and database
print(type(con))

# 2. cursor 객체 생성
# cursor : 작업관리자(해석)
cur = con.cursor()


def newPosting(content, tags):
    result = None
    try:
        # 본문추가
        cur.execute("INSERT INTO post(content) VALUES(?)", [content])
        result = cur.lastrowid  # 마지막으로 insert된 row의 id를 가져온다.

        # 해시태그 검사
        for tag in tags:

            tag_id = findTag(tag)

            # 사용된 해시태그 + 1
            cur.execute("UPDATE POOL SET CNT = CNT + 1 WHERE ID = ?", [tag_id])
            # 포스트 + 사용된 해시태그 이력 남기는 부분
            cur.execute("INSERT INTO TAGS VALUES(?, ?)", [result, tag_id])

        con.commit()  # commit을 해야 실제로 DB에 반영된다.

    except Exception as e:
        print("에러 발생:", e)
    con.rollback()
    return None

    return result


# tag를 입력받아 pool에서 검사
# tag가 없으면 추가, 있으면 id 가져오기
# 리턴 id
def findTag(tag):
    cur.execute("SELECT id FROM pool WHERE name LIKE ?", [f"%{tag}%"])
    result = cur.fetchall()

    if len(result) == 0:
        cur.execute("INSERT INTO pool(name) VALUES(?)", [tag])
        tagid = cur.lastrowid
    else:
        tagid = result[0][0]  # 첫 번째 결과의 첫 번째 열을 반환

    return tagid


# 게시물 불러오기
def findPost(content=None):
    if not content:
        cur.execute("SELECT * FROM post")
    else:
        cur.execute("SELECT * FROM post WHERE content LIKE ?", [f"%{content}%"])
    result = cur.fetchall()
    return result


def findPostByContent(content):
    cur.execute(
        """
                select id from post where content like ?
                """,
        [f"%{content}%"],
    )

    result = cur.fetchone()
    print(f"result: {result[0]}")
    if result:
        return result[0]


# 게시물 불러오기
def findHashTag(tag=None):
    if not tag:
        cur.execute("select id, name, cnt from pool order by cnt desc, name asc")
    else:
        cur.execute(
            "select id, name, cnt from pool where name like ? order by cnt desc, name asc",
            [f"%{tag}%"],
        )
    result = cur.fetchall()
    return result


def loadPost(post_id=None):

    cur.execute(
        """
                select * from post where id = ?
                """,
        [post_id],
    )
    post = cur.fetchone()[0]

    if not post:
        return None

    cur.execute(
        """
                select p.name from tags t
                inner join pool p on t.pool_id = p.id
                where t.post_id = ?
                """,
        [post_id],
    )

    tags = ["#" + row[0] for row in cur.fetchall()]
    return (post, tags)


###################### 질문 수정 ##########################
def updatePost(post_id, content, new_tags):
    if post_id:
        try:
            print(f"new_content: {content}")
            cur.execute(
                """
                            update post set content = ? where id = ?
                            """,
                [content, post_id],
            )
            result = cur.lastrowid

            # 사용된 태그
            cur.execute(
                """
                            select p.name from tags t
                            inner join pool p on t.pool_id = p.id
                            where t.post_id = ?
                            """,
                [post_id],
            )
            related_tags = [row[0] for row in cur.fetchall()]
            # ['해시태그1', '해시태그2', '해시태그3']

            # 수정할 태그들에 해당 게시물에 사용된 기존 태그가 없을 때
            for original_tag in related_tags:
                if original_tag not in new_tags:
                    delete_tag_id = findTag(original_tag)
                    # 태그 삭제
                    cur.execute(
                        """
                        delete from tags where post_id = ? and pool_id = ?
                        """,
                        [post_id, delete_tag_id],
                    )
                    # 태그 사용 횟수 다시 차감
                    cur.execute(
                        """
                        update pool set cnt = cnt - 1 where id = ?
                        """,
                        [delete_tag_id],
                    )

            # 해당 게시물에 새로운 태그들 추가
            for tag in new_tags:
                if tag not in related_tags:
                    tag_id = findTag(tag)
                    print(f"추가할 태그 id: {tag_id}")

                    # 사용된 해시태그 + 1
                    cur.execute("UPDATE POOL SET CNT = CNT + 1 WHERE ID = ?", [tag_id])
                    # 포스트 + 사용된 해시태그 이력 남기는 부분
                    cur.execute("INSERT INTO TAGS VALUES(?, ?)", [post_id, tag_id])

            con.commit()
        except:
            con.rollback()
    else:
        return None


###################### 태그 수정 ##########################
########## 태그 풀에서 해당 태그 ID 가져오기
########## 태그 풀에서 해당 태그 수 증감하기


# newPosting("새 게시물", ["해시태그1", "해시태그2", "해시태그3"])
# print(findPost("게시물"))
# print(findHashTag())
# print(findHashTag("1"))

updatePost(
    findPostByContent("수정"),
    "두번째수정입니다",
    ["수정해시태그1", "수정해시태그2", "수정수정해시태그3"],
)
