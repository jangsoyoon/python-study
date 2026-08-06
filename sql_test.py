import sqlite3
from tarfile import data_filter

# 1. 데이터베이스 연결
# connect() - close() 이 한 쌍
# connect -> File Open -> close
# con = sqlite3.connect(':memory:')  # Create an in-memory database
con = sqlite3.connect("test.db")  # Create and atabase
# print(help(sqlite3.connect))
# print(type(con))

# con.execute -> 1개의 SQL 문을 실행
# con.executemany -> 1개의 SQL 문을 반복해서 실행
# con.executescript -> 한번에 여러개의 SQL 문을 실행 (비표준, 되도록 쓰지 X)

# 2. cursor 객체 생성
# cursor : 작업관리자(해석)
cur = con.cursor()

# print(type(cur))Ò
# print(dir(cur))'

# 3. SQL 실행을 요청 -> execute
# cur.execute('''``
#             CREATE TABLE IF NOT EXISTS test (
#                 no Integer,
#                 name char(1)
#             );
#             ''')
# cur.execute('''
#             drop table if exists part;
#                 ''')

# cur.executescript('''
#             CREATE TABLE IF NOT EXISTS city (
#                 cno Integer primary key,
#                 name varchar(100) default '도시'
#             );

#             CREATE TABLE IF NOT EXISTS supplier (
#                 sno Integer primary key,
#                 name varchar(100) default '지점',
#                 cno integer not null
#             );
#             CREATE TABLE IF NOT EXISTS part (
#                 pno Integer primary key,
#                 name varchar(100) default '아메리카노'
#             );
#             CREATE TABLE IF NOT EXISTS sells (
#                 sno integer not null,
#                 pno integer not null,
#                 price integer not null
#             );
#             ''')


# data = [
#     (1, '성북구'),
#     (2, '분당구'),
#     (3, '동대문구'),
#     (4, '강북구')
# ]
# coffee = [
#     ('아메리카노',),
#     ('카페라떼',),
#     ('바닐라라떼',)
# ]
# cur.executemany('''
#             INSERT INTO part(name) VALUES (?);
#             ''', coffee)

# cur.execute('''
#             INSERT INTO city VALUES (null, '강북구');
#             ''')
# cur.execute('''
#             INSERT INTO city(cno, name) VALUES (:cno, :name);
#             ''', {'cno': None, 'name': '중랑구'})

# person = {'no': 1, 'name': '아무개'}
# persons = [
#     {'no': 2, 'name': '홍길동'},
#     {'no': 3, 'name': '김철수'},
#     {'no': 4, 'name': '이영희'}]

# cur.executemany('''
#             INSERT INTO test VALUES (:no, :name);
#             ''', persons)

# cur.execute('''
#             select * from city where name like?;
#             ''', ('%동대문%',))

# cur.execute('''
#             update city set name = '서초구' where cno = 6;
#             ''')

# cur.execute('''
#             select * from part;
#             ''')

city = "강남"
supplier = "강남1호점"

# cur.execute('''
#             select cno from city where name like ?;
#             ''', ('%' + city + '%',))
# cno = cur.fetchone()[0]

# cur.execute('''
#             insert into supplier(sno, name, cno) values(null ,?, ?)
#             ''',[supplier, cno])
# cur.execute('''
#             insert into supplier(name, cno) values(?, (
#                 select cno from city where name like ?
#                 order by cno asc
#                 limit 0, 1
#             ))
#             ''',[supplier, '%' + city + '%'])

# cur.execute('''
#             delete from sells;
#             ''')

# cur.execute('''
#             select * from sells;
#             ''')

priceData = [
    {"sname": "%안암%", "pname": "아메리카노", "price": 3000},
    {"sname": "%안암%", "pname": "카페라떼", "price": 3000},
    {"sname": "%강남%", "pname": "아메리카노", "price": 4000},
    {"sname": "%강남%", "pname": "카페라떼", "price": 3500},
    {"sname": "%강남%", "pname": "바닐라라떼", "price": 5000},
]

# cur.executemany('''
#             insert into sells(sno, pno, price) values(

#                 (select sno from supplier where name like :sname limit 0, 1),
#                 (select pno from part where name like :pname limit 0, 1),
#                 :price
#             )
#             ''', priceData)


# cur.execute('''
#             select c.cno, c.name, s.name from city c
#             join supplier s on c.cno = s.cno;
#             ''')


cur.execute("""
            select c.name, count(s.name) from city c
            join supplier s on c.cno = s.cno
            group by c.name
            """)

cur.execute("""
            select p.name, avg(s.price) sp from sells s
            join part p on s.pno = p.pno
            group by p.pno
            order by sp desc
            """)

# 판매 갯수가 큰거
cur.execute("""
            select p.name, sum(s.price) sp from sells s
            join part p on s.pno = p.pno
            group by p.pno
            order by sp desc
            """)


cur.execute("""
            select c.name, s.name, p.name, a.price from sells as a
            inner join part as p
            on p.pno = a.pno
            inner join supplier as s
            on s.sno = a.sno
            inner join city as c
            on c.cno = s.cno
            order by c.cno, s.sno, p.pno asc
            """)

# 판매되지 않은 곳도 나오게

cur.execute("""
            select c.name, s.name, p.name, a.price from city c
            join supplier s on c.cno = s.cno
            join sells a on s.sno = a.sno
            join part p on a.pno = p.pno
            order by c.cno, s.sno, p.pno asc
            """)


# print(cur.fetchone()[0]) # fetchone() - fetchall() 이 한 쌍


# 4. SQL 결과를 요청 -> fetch
print(cur.fetchall())


# con.execute("""
#             CREATE TABLE track (
#             id INTEGER PRIMARY KEY,
#             title TEXT,
#             length INTEGER,
#             rating INTEGER,
#             count INTEGER DEFAULT 0,
#             album_id INTEGER NOT NULL,
#             FOREIGN KEY (album_id) REFERENCES album(id)
#             );
#             """)


con.commit()  # commit() - rollback() 이 한 쌍
con.close()  # connect() - close() 이 한 쌍
