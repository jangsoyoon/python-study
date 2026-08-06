from types import MethodDescriptorType
from typing import Any

import matplotlib.pyplot as plt
import tensorflow as tf
import inspect
import keyword

# lambda 매개변수 : 표현식
# 오른쪽은 식이 올 수 있다.
# 파이썬은 모든 것이 객체이다.
# a = print 도 가능하다.
# 파이썬의 가장 기본적인 형식은 튜플이다.
# -> a = 1,2,3,4 -> 괄호 생략해도됨... a = (1,2,3,4) 로 해도 되긴 함.

# lamda_hello = lambda name: print("Hello", name)
# lamda_hello("soyoon")

# lamda_cal1 = lambda x, y: print(x + y)
# lamda_cal1(3, 5)

# lamda_list = lambda x: [(i * 2) for i in range(x)]
# print(lamda_list(5))

# leg = int(input('변의 길이: '))
# print(leg)

# a = print
# a("Hello expression")


# a, b, *c = 1, 2, 3, 4, 5
# print(a, b, c)
# 1 2 [3, 4, 5]


# (x_train, y_train), (x_test, y_test) = mnist.load_data() 여기에서 mnist.load_data()의 값은 2개라고 생각된다.
# (x_train, y_train), (x_test, y_test) = a, b 로 대체될 수 있는데 그럼 여기에서 a의 값은 얼마일까?
# -> a의 값도 2개이다(x_train, y_train의 값의 수를 맞춰야해서).
# numpy, tensor ....
# atomic <> container 쪼갤 수 있다 <> 쪼갤 수 없다
# sequence <> nonsequence 순서가 있다 <> 순서가 없다
# 문자는 sequence이다. 순서가 있다. a[0] = 'a' a[1] = 'b' a[2] = 'c' a[3] = 'd' indexing 가능하다. slicing 가능하다. a[0:2] = 'ab' a[1:3] = 'bc' a[2:4] = 'cd'
# immutable 은 문제가 없다.


# plt.bar([1,2,3,4,5], [1,2,3,4,5], width = 0.5, color = 'pink')
# plt.show()


# def x(a, b=3):
#     return a + b


# print(x(a=2))  # keyword argument


# def xxxx(a: str) -> str:
#     return a


# print(xxxx("soyoon"))

# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# result = [n for n in numbers if n % 2 == 0]

# print(result)

# print(inspect.getsource(x)) # 함수의 소스코드를 가져올 수 있다.


# a = range(100)

# b = []
# for i in a:
#     b.append(i + 10)
# print(b)

# comprehension 방식
# c = [i + 10 for i in a]  # 위의 for문과 같은 의미이다.
# print(c)

# for i in range(10):
#     print(i)
#     print(i + 10)


# a = {"x": 1, "y": 2}
# b = {"z": 3, "x": 4}

# print({**a, **b})  # {'x': 4, 'y': 2, 'z': 3} a의 x값이 b의 x값으로 덮어씌워진다.


# print(3 * "abc")


# a = list("abc")  # ['a', 'b', 'c']
# print(a)
# print(3 * a)


# for -> iterable
# comp ->
# map -> func + iterable


# f = map(
#     lambda x: x + 10, [1, 2, 3, 4, 5]
# )  # map은 iterable을 반환한다. list로 감싸야 한다.

# print(list(f))  # [11, 12, 13, 14, 15]


# try:
#     a = input()
#     b = int(a) + 10
# except:
#     print("다시")

# 존재의 유무에 따라 참 거짓을 판단한다.
# a = print
# if a:
#     print("a")
# else:
#     print("b")


# def x(a):
#     print(a)
#     return a


# and : 앞의 것이 참이면 뒤에것 반환 / 앞의 것이 거짓이면 앞의 값을 그대로 반환
# print(3 and 4)
# or : 앞이 것이 참이면 앞에것, 앞에 것이 거짓이면 뒤에것 반환
# x(a or 4)
# print(1 or 3)

# a == 1 or a == 2 or a == 3 -> 1 의 식과 같다.
# print(3 in [1, 2, 3])


# help , dir 치면 설명 나옴
# print(dir(keyword))
# a = 2

# b = 3 if a > 2 else 4
# # x(3 if a > 2 else 4)
# b = [1, 2, 3]

# for i in b:
#     if i == 3:
#         break
#     print(i)
# else:
#     print("end")


# 예외처리
# 문제가 일어났는데 계속 돌아가면 더 문제가 생겨서 중간에 그만두게 하기 위해

# a = 1
# assert
# assert a == 2, "야 너 1이야"

# raise
# if a > 1:
#     raise ZeroDivisionError
# else:
#     print("a")

# 문제가 일어나도 시스템은 계속 돌아가야하기 때문에
# 에러가 나면 except 부분으로 넘어감 (중단 안됨)
# 에러가 안 나면 else -> 그리고 마지막으로 finally

# try:
#     a = 2
# except:
#     print("error Message")
# else:
#     print("b")
# finally:
#     print("c")


# 'a' 를 넣으면 에러가 나기 때문에 try 부분으로 다시 돌아감 -> 입력을 제대로 했을 때 else 부분으로 가서 끝남.
# while 1 == 1:
#     try:
#         a = input()
#         b = int(a) + 10
#     except:
#         continue
#     else:
#         print(b)
#         break

# else 는 for, while, if 뒤에 붙음.

# 익명 함수
# lambda
# a = lambda x: x + 1
# a = lambda x: x + 10
# print(a(3))
# a = lambda x: x + 10
# print(a(3))

# __call__ 이 있다면 함수처럼 생각할 수 있다. -> 괄호 붙일 수 있다
# print(dir(a))


##### ???????????????????? 심화공부
# a = [print]
# a[0]("sun")
# ## a[0] = print  -> print("sun")

# do_it = lambda f, *args: f(*args)


def x(fun, *ar):
    return fun(*ar)


# print(x(sum, [1, 2, 3, 4]))

# x(add, 1, 2, 3)     → ar = (1, 2, 3)          # 3개 뭉침
# x(add, [1,2,3])      → ar = ([1,2,3],)         # 1개(리스트) 뭉침
# x(add, [1,2,3], 4)   → ar = ([1,2,3], 4)       # 2개 뭉침

# def y(fun):
#     fun("sun")


# x(print)
# meta class


# print = 3

## global 인 print 삭제
# del print

# print("aa")


# class A:
#     x = 0
#     pass


# A.x = 1
# print(A.x)


# [] 리스트 = "바뀔 수 있는 데이터 모음"
# () 튜플 = "고정된, 안 바뀌는 값들의 묶음"


# class 를 인스턴스화
# class에는 값과 기능이 정의되어있음
# instance는 구체적인 값
# instance화 : class 이름에 () 붙여서 함수처럼 사용하는 것


# class A:
#     x = 1  # 클래스 변수 class variable

#     def __init__(self, x):  # instance method
#         self.x = x  # instance 변수 instance variable self
#         print(x)

#     def tt(self):
#         print("B")

#     @classmethod
#     def ss(cls):
#         print("C")


# a = A(8)
# print(a.x)
# print(A.x)
# print(vars(a))

# print(A.x)
# A.ss()
# A().tt()

# a = A()
# 인스턴스는 인스턴스에 해당 ss함수가 없으면 클래스꺼로 찾아온다.
# 그래서 인스턴스화 하면 다 쓸 수 있다..
# a.ss()

# 인스턴스 변수도 인스턴스에 없으면 클래스꺼로 찾아온다.
# print(a.x)


class B:
    pass


# 기본적인 상속 때문에 기능을 한다.
# class B(object):  -> (object) 생략된거임
# a = B()
# B.x = 1
# print(a.x)
# print(vars(A))

# INFO! 중간마다 값이 계속 바뀔 수 있다...   -> *처음부터 선언해버려야(인스턴스 내에서) 중간 값이 변경되는 일이 없어진다.*
# b = B()
# print(b.x)
# B.x = 5
# print(b.x)


# class A:
#     def __init__(self) -> None:
#         print("A")

#     def __call__(self, *args: Any, **kwds: Any) -> Any:
#         print("B")

#     @staticmethod
#     def tt(a, b):
#         return a + b


# def x():
#     return 1


# x = 3
# 이게 왜 TypeError: 'int' object is not callable 이 에러나 났냐미연 .
# -> x라는 이름에 함수 객체를 바인딩했는데 x = 3이라고 값을 덮어씌웠기 때문에
# 더 이상 함수 호출이 불가능하다.

# print(x())

# s = A()
# ## __call__ 이 있으면 인스턴스() 가능하다 ex.s()  -> dir(s) 해보고 나서 할 것
# # print(dir(s))
# s()
# print(A.tt(2, 6))


########## static method ###########


# class C:
#     @property
#     def tt(self):
#         print("tt")


# c = C()
# c.tt


# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     @classmethod
#     def from_string(cls, text):
#         name, age = text.split(",")
#         return cls(name, int(age))


# p = Person.from_string("Tom,20")
# t = Person.from_string("Jang, 30")

# print(p.name)
# print(t.name)

# * 다중상속
# class A(B,C,D):
#     def desc(self):
#         print("바보")

#     pass


# x = A(3)
# x.desc()


# xx = A()
# xx.aa()
# print(vars(xx))  # {'x': 1, 'y': 2}


# ----------> 오버라이딩
# class A:
#     def __init__(self) -> None:
#         self.x = 1

# class B(A):
#     def __init__(self) -> None:
#         self.x = 2

# ----------> 오버라이딩


class X:
    def __init__(self) -> None:
        print("A")


class Y(X):
    def __init__(self) -> None:
        super().__init__()


print(vars(Y))

# * Function / Method
# * 1. class 안에 정의 여부
# * 2. method 는 첫번째 self 무시
# * 3. function은 외부에서 접근 불가 / method는 가능
# * 클래스 입장에선 함수 / 인스턴스 입장에서는 method


class A:
    def tt(self):
        print("A")


a = A()
a.tt()
A.tt(a)
