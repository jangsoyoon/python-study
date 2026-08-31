import numpy as np

from scipy.datasets import face
import torch

# a = torch.Tensor([1, 2, 3])
# for x in dir(a):
#     if "array" in x:
#         print(x)

# print([x for x in dir(a) if "array" in x])
# dir(a)

a = np.array([1, 2, 3])
# print(type(a))  # <class 'numpy.ndarray'>
#! https://numpy.org/doc/stable/user/quickstart.html
#! 2,(3,4) -> 2,x 로 봤을 때 x가 두개있다 => 3,4가 두개 있다
#! 2,3 이 4개가 있다 // 2,4 가 3개가 있다  # 우유곽으로 차원계산하는 거 익숙해질것..
x = np.arange(24).reshape(2, 3, 4)
x.size
# x.size 를 모르더라도 x.shape 만 알면 알 수 있다.
x.shape


import matplotlib.pyplot as plt

# im -> image 줄인말
t = plt.imread("/Users/ddoyoon/Downloads/IMG_4771.JPG")

# 나 지금 몇차원인지 알고싶어
t.ndim
# 이미지 사이즈 + 차원
t.shape

# 데이터 타입 알고싶어
t.dtype

# 이미지 잘라짐
# plt.imshow(t[100:300, 200:300, :])
# # 색깔 반대
# plt.imshow(t[100:300, 200:300, ::-1])
# # 좌우반대
# plt.imshow(t[100:300, ::-1, :])
# plt.show()

a = np.zeros((3, 4))
# * a와 똑같은 모양(shape)과 자료형(dtype)을 가진 배열을, 값은 전부 0으로 채워서 새로 만드는 함수
b = np.zeros_like(a)
# print(a)
# print(b)

# 2,3 행렬 4로 채우고 싶어
np.full((2, 3), 4)

# 둘의 차이가 뭘까? 아래에서 설명..
# a = 1
# print(a)


class X:
    def __repr__(self) -> str:
        print("repr")
        return "abc"

    def __str__(self) -> str:
        print("str")
        return "bcbb"


aa = X()
# 이름을 불렀을 때 return값이 있다 / print 치면 return값이 없다.
# print(aa)
# t = print(aa)
# print(t)  # 값이 없다 -> None 이 나옴

import tensorflow as tf

a = tf.constant([1, 2, 3])
# 둘의 결과가 다름 (a를 불렀을 때와 print(a)했을 때와 // 나는 ide를 쓰고 있어서 repr(a) 로 print 하면 됨)
# a
# print(a)
#  -> 만드는 사람마다 표현 방식이 다르다

#! 외워야되는 5가지 테크닉 (slicing)

a = np.array([[1, 2, 3], [4, 5, 6]])
# print(repr(a))
#! 1. , 를 활용할 수 있다
# a[0][2] == a[0,2]
#! 2. 조건을 둘 수 가 있다
list(filter(lambda x: x > 2, [1, 2, 3]))
a = np.array([[1, 2, 3], [4, 5, 6]])
aa = np.array([1, 2, 3])
# a[lambda x: x>3] # 불가능
# aa[lambda x: x>3] # 불가능
# aa[aa>1] # 가능


# a > 1  # 2차원으로 나옴
# a[[[True, True, False], [False, False, True]]]  # 불가능
# a[
#     np.array([[True, True, False], [False, False, True]])
# ]  # 가능 데이터타입까지 맞췄기 때문에(np.array)
# a[a > 1]  # 1차원으로 바뀌었다. filter 처럼 flatten 으로 차례대로 하나씩 들어가서

# print(a[[0]])

#! 3. fancy indexing이 가능하다
# tips = sns.load_dataset('tips')
# tips.tip + 5 # 이게 왜 연산이 될까? -> broadcasting이 되기 때문에
# tips.tip #1차원
# tips[['tip']] # [] 를 한번 더 씌우면 차원을 유지시켜준다 -> fancy indexing (새로운 데이터셋을 만들 수 있다)
# tips[tips.tip>3] # numpy에서 나오는 것이고 이렇게도 사용할 수 있다

#! 4. 아래와 같은 예시도 가능하다
a[(0, 1), (0, 1)]  # 0에 0열, 1에 1열
a[[0, 1], [0, 1]]
# 두개의 결과는 같으나 좌표적으로 조금 다르다 ...


#! 5.  ...
a[0] = a[0][:] = a[0, :]
a[:, :] = a[...]

b = np.arange(24).reshape(2, 3, 4)
b[..., 0]
c = b[..., 0, :]
# print(c)
a[None] = a[np.newaxis]  # 차원이 증가된다. 즉 np.newaxis = None


a = np.arange(6).reshape(2, 3)
# a[np.newaxis] = (1, 2, 3)
# a[:, np.newaxis] = (2, 1, 3)
# a[..., np.newaxis] = (2, 3, 1)


b = np.arange(6).reshape(3, 2)
#! 통계는 기본적으로 reduction

a = np.arange(24).reshape(4, 6)
# axis none -> 0차원
a.sum()

b = a.ravel  # => 메모리 공유
b = a.flatten()  # copy
# mutableDataSet 에서 생긴다

# a = [1, 2]  # mutable data
# b = a
# b[0] = 100
# print(a)
# a = [1, 2]
# b = a[:] # [:] 이렇게 하면 메모리 공유 안한다 -> a[:] = copy # 중간 중간 copy 를 해서 체크리스트? 를 만든다.
# b[0] = 100
# print(a)


# 그럼 2차원은 어떨까?

a = [[1, 2], [3, 4]]
b = a
b[0][0] = 100
# print(a)

a = [[1, 2], [3, 4]]
b = a[:]
b[0][0] = 100
# print(a)

a = [[1, 2], [3, 4]]
b = a.copy()
b[0][0] = 100
# print(a)
#! 왜 값이 똑같을까? - shallow copy 얕은 카피
import copy

a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)
b[0][0] = 100
# print(a)


#! numpy 에서는 copy -> 기본이 deepcopy 이다.
#! numpy 에서는 얕은(shallow) copy -> view
id(a)  # 메모리 확인
a = np.arange(10).reshape(2, 5, order="F")  # order = 'C' 가로로 정렬 / 'F' 세로로 정렬

a = 1
a = 2  # 재할당 이름이 같은데 값이 달라지는 것

b = [1, 2, 3]
b.append(
    4
)  #! -> inplace 라는 것 . 리턴값은 없지만 값이 바뀌는 것. mutable 이라서 생기는 일.
# 리턴값은 없지만 값이 바뀌는 것 / 리턴값이 있지만 값이 바뀌지 않는 것 / 리턴값도 있고 바뀌는 값도 있는 것
# 재할당할 경우에는 inplace = False를 해야 리턴값이 생김

# a = np.arange(10)
# print(a)
# print(a.reshape(2, 5))
# print(a)
# #! reshape 는 immutable 이기 때문에 재할당을 해야함
# a = np.arange(10).reshape(2, 5)
# print(a)

a = np.arange(24).reshape(4, 6)
# print(a)
a.sum()

# [1,2,3] + [4,5,6]
# print(np.add(a, 4))

from scipy import misc
import torch

# print(face().shape)

import seaborn as sns

tips = sns.load_dataset("tips")

tips["size"]
# print(tips[["sex", "smoker"]])

a = torch.arange(24).reshape(4, 6)

# zero padding
#  [[ 0  1  2  3  4  5]
#  [ 6  7  8  9 10 11]
#  [ 0  0  0  0  0  0]
#  [ 0  0  0  0  0  0]]
a = np.arange(12)
a.resize(4, 6)  # -> 메소드는 deprecated 됐지만 함수는 살아있다 np.resize
# print(np.resize(a, (4, 6)))
# print(a)

x = np.arange(24).reshape(4, 6)
y = np.arange(24).reshape(4, 6)
np.vstack((x, y))  # 추가되는 데이터를 합칠 때 (차원유지)
np.hstack((x, y))  # 쪼개져있는 데이터를 합칠 때 (차원유지)
np.dstack((x, y))  # 차원을 증가시켜서 n차원 만들 때 / 잘 안 씀
np.stack((x, y))  # 차원을 증가시켜서 붙인다
print(np.row_stack((x, y)))
print(np.column_stack((x, y)))

np.r_[x, y]
np.c_[x, y]

import pandas as pd

pd.read_csv
# * np.rec.array -> pandas 로 쉽게 사용가능하다

# # 행 백터
# row = np.array([1, 2, 3])

# # 열 백터
# col_1 = np.array([[1], [2], [3]])

# col_2 = np.array([[1, 2, 3]])

# # 행렬 생성
# matrix_1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# matrix_2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
# print("행 백터")
# print(row)
# print("열 벡터1")
# print(col_1)
# print("열 벡터2")
# print(col_2)
# print("행렬1")
# print(matrix_1)
# print("행렬2")
# print(matrix_2)

# number_one = np.ones((4, 2))
# print(number_one)
