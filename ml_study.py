from sklearn.datasets import load_wine
from sklearn.datasets import load_breast_cancer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neural_network import MLPClassifier
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
import pandas as pd

data = load_wine(as_frame=True)
# print(data.DESCR)
wine = data.frame
# print(wine.info())
# print(wine.describe())
win_no_class = wine.iloc[:, :-1]
# win_no_class.describe()
# win_no_class.boxplot(figsize=(14, 3))
# win_no_class.iloc[:, :-1].boxplot(figsize=(14, 3))
# plt.show()

# sns.pairplot(wine, hue="target")
# plt.show()

data = load_breast_cancer(as_frame=True)
# print(data.frame.info())
iris = sns.load_dataset("iris")
# print(iris.info()) # 5개의 column, 150 개의 데이터

#! EDA? -> 탐색적 데이터 분석 / 데이터를 본격적으로 모델링하거나 가설을 검정하기 전, 다양한 각도에서 관찰하고 이해하는 기초 분석 과정
#! learning curve?
# sns.pairplot(iris, hue="species")
# plt.show()

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

# 1. iris 종류 구분하고 싶다
# 2. ML
# 3. Data가 있어야함
# 4. 대표성이 있어야함 (남 여 구분하고 싶은데 데이터가 노트북의 종류라면? (맥북인지, 무식한 노트북인지) -> 대표성 부족)
# 5. 평가
# 6.

data = load_iris(as_frame=True)
iris = data.frame
a = data.frame.corr()
# sns.heatmap(a, annot=True)
# plt.show()
from sklearn.model_selection import train_test_split  # holdout

# * keep 값	의미
# * 'first' (기본)	첫 번째만 봐줌(False), 나머지는 True
# * 'last'	마지막만 봐줌(False), 나머지는 True
# * False	아무것도 안 봐줌, 중복된 건 전부 True
iris[iris.duplicated(keep=False)]
# print[iris.duplicated()]
# ! [:, :-1] 불일치한 데이터셋 확인하기 위해 - target이 다를 수 있어서 target 컬럼 빼고 중복 체크한 거임.
# print(iris.iloc[:, :-1].duplicated(keep=False))
#! 중복 데이터 제거 - data leakaging 문제 해결
#! 체크 방법	잡아내는 것
#! iris.duplicated() (전체)	모든 값(feature+target)이 완전히 똑같은 "진짜 완전 중복"
#! iris.iloc[:, :-1].duplicated() (target 제외)	측정값은 같은데 라벨(정답)만 다른, 데이터 오류 의심 사례
from sklearn.model_selection import train_test_split  # holdout

iris.drop_duplicates(inplace=True)
# ! X_train  → 학습용 features (feature 데이터의 80%)
# ! X_test   → 시험용 features (feature 데이터의 20%)
# ! y_train  → 학습용 정답 (X_train에 짝지어지는 target 80%)
# ! y_test   → 시험용 정답 (X_test에 짝지어지는 target 20%)
X_train, X_test, y_train, y_test = train_test_split(
    iris.iloc[:, :-1],  # X (features)
    iris.target,  # # y (정답)
    test_size=0.1,  # 20%는 테스트용으로 떼어놓기
    stratify=iris.target,
)
lr = LogisticRegression()
# # ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)',
# #    'petal width (cm)', 'target'],
# # :-1 이 target 빼고 집어넣으면 iris.target 이 나오는~~~
# ! fit = "공부해라(학습해라)" — 데이터를 보고 패턴을 찾아내는 단계
# ! predict = "문제 풀어봐라(예측해라)" — 학습한 걸 바탕으로 새로운 데이터의 답을 맞혀보는 단계
lr.fit(X_train, y_train)
# print(lr.predict(X_test) == y_test)

# 정확도 비율..?
# print(lr.score(X_test, y_test))

# # print(iris.columns)
# result = lr.predict([[1, 5, 13, 2]])
# print(result)

gn = GaussianNB()
# gn.fit(iris.iloc[:, :-1], iris.target)
# ! 예측값만 나온다
gn.fit(X_train, y_train)
# ! 이 모델이 얼마나 잘 맞히는지, 성적을 숫자 하나로 알려주는 함수
gn.score(X_test, y_test)

#! score 확률이 run할 때마다 달라지는데 그 이유 -> 데이터가 적어서

# result = gn.predict([[1, 5, 13, 2]])
# print(result)

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
# print(y_train)
# print(np.histogram(y_train, bins=10))

mpg = sns.load_dataset("mpg")
# print(mpg.info())

# print(mpg.isnull())
# print(mpg.isna().any())
# ! 리턴값은 없지만 값이 바뀌는 것. mutable 이라서 생기는 일.
# ! 리턴값은 없지만 값이 바뀌는 것 / 리턴값이 있지만 값이 바뀌지 않는 것 / 리턴값도 있고 바뀌는 값도 있는 것
#! 데이터 불러올 때마다 확인해서 바꿔야하나 ? -> read_csv() 에 받아올 때 데이터를 미리 처리할 수 있다.
# print(mpg[mpg.horsepower.isna()])
# ! float('nan') =! nan
# print(mpg.loc[32].horsepower is None)
# ! => masked array 기법
# ! None 을 집어넣으면 연산 자체가 안됨 -> 이건 값이 없는 거다 라고 표시를 해준다 (실제 값이 있을 수도 있다)
a = np.ma.array([1, 2, 3], mask=[True, False, True])

b = np.array([None, 1, 2])
# ! -> 넣으면 object 로 인식된다. 숫자를 넣었는데도 -> 호모지니어스(동질성) 때문에 그래서 Nan 이라고 해서 넣는다.
# ! nan 을 0으로 다 바꾼다
# print(mpg.horsepower.fillna(0))

# print(mpg.horsepower.sum())
# print(mpg.origin.unique())

# ! 그림을 그릴 수 있는 구조체가 될 수 있다 해당 컬럼들이 x축이 되고 값이 y축
# print(mpg.origin.value_counts())
# mpg.origin.value_counts().plot.pie()
# plt.show()

le = LabelEncoder()
# le.fit(mpg.origin)
# le.transform(mpg.origin)
# print(le.fit_transform(mpg.origin))
# le.inverse_transform([0,1,2])
oe = OrdinalEncoder()
# print(oe.fit_transform(mpg.origin.values.reshape(-1, 1)))
# * 더미변수를 만들어주세요

import missingno as mino

pd.get_dummies(mpg["origin"])

dir(mino)
mino.matrix(mpg)
titanic = sns.load_dataset("titanic")

titanic.sex.value_counts()
# titanic[titanic.sex == 'female'].survived.sum()
titanic[titanic.sex == "female"][["survived"]]

# print(titanic.groupby("sex")[["survived"]].sum() / len(titanic))

# print(titanic.columns.values)

breast = load_breast_cancer(as_frame=True).frame


# breast.boxplot()

X_train, X_test, y_train, y_test = train_test_split(
    breast.iloc[:, :-1], breast.target, random_state=1
)
lr = LogisticRegression()

lr.fit(X_train, y_train)
print(lr.score(X_test, y_test))
from sklearn.preprocessing import StandardScaler

ss = StandardScaler()

breast_std = breast.copy()

breast_std[["worst area"]] = ss.fit_transform(breast[["worst area"]])

plt.figure(figsize=(15, 6))
breast_std.boxplot()
# plt.show()

X_train, X_test, y_train, y_test = train_test_split(
    breast_std.iloc[:, :-1], breast_std.target, random_state=1
)
lr_ = LogisticRegression()
lr_.fit(X_train, y_train)
# print(lr_.score(X_test, y_test))


# # 머신러닝 수업 전체 정리

# 전체 코드가 하는 일을 한 줄로 요약하면:
# **"데이터를 불러오고 → 살펴보고(EDA) → 문제 있는 부분 고치고 → 학습/시험용으로 나누고 → 모델을 학습시키고 → 점수를 확인한다"**

# 이 순서를 계속 반복하고 있어요. 이 순서 자체가 머신러닝의 기본 뼈대이니, 이것부터 외워두시면 좋아요.

# ```
# 1. 데이터 불러오기
# 2. EDA (탐색적 데이터 분석) - 데이터를 살펴보기
# 3. 데이터 정제 - 중복 제거, 결측치 처리, 인코딩, 스케일링
# 4. Train/Test 분리
# 5. 모델 학습 (fit)
# 6. 평가 (score, predict)
# ```

# ---

# ## 1. EDA (탐색적 데이터 분석)이란

# ```python
# #! EDA? -> 탐색적 데이터 분석 / 데이터를 본격적으로 모델링하거나
# # 가설을 검정하기 전, 다양한 각도에서 관찰하고 이해하는 기초 분석 과정
# ```

# **본격적으로 모델을 학습시키기 전에, "이 데이터가 어떻게 생겼는지" 먼저 눈으로 확인하는 단계**예요. 무작정 모델부터 돌리면, 이상한 데이터(결측치, 중복, 이상치)가 섞여 있어도 모르고 지나갈 수 있어요.

# ### 이 수업에서 쓴 EDA 도구들

# | 도구 | 하는 일 |
# |---|---|
# | `.info()` | 컬럼 이름, 데이터 타입, 결측치 개수 등 요약 정보 |
# | `.describe()` | 평균, 최솟값, 최댓값 등 통계 요약 |
# | `.corr()` + `sns.heatmap()` | 컬럼들 사이의 상관관계를 색깔로 보기 |
# | `.boxplot()` | 각 컬럼의 분포(중앙값, 이상치)를 상자 모양으로 보기 |
# | `sns.pairplot(hue="target")` | 모든 feature 쌍을 산점도로 그려서, 품종(target)별로 색을 다르게 표시 → 어떤 feature 조합이 분류에 잘 먹히는지 눈으로 확인 |
# | `mino.matrix(mpg)` (missingno) | 결측치가 어디에 얼마나 있는지 한눈에 그림으로 보기 |

# **핵심: 이 도구들은 전부 다 "모델 학습 전에 데이터를 미리 훑어보는" 용도예요.** 코드에 `#`으로 많이 주석 처리된 게 보이는데, 이런 EDA는 "확인만 하고 실제 파이프라인에는 안 넣는" 경우가 많아서 그래요.

# ---

# ## 2. 데이터의 "대표성" — 아주 중요한 개념

# ```python
# # 4. 대표성이 있어야함 (남 여 구분하고 싶은데 데이터가 노트북의 종류라면?
# # (맥북인지, 무식한 노트북인지) -> 대표성 부족)
# ```

# **"내가 풀려는 문제와 상관없는 데이터로는 절대 좋은 모델을 만들 수 없다"**는 뜻이에요.

# 예: "성별을 구분하고 싶다"면서 "노트북 브랜드" 데이터를 준다면? 노트북 브랜드는 성별과 아무 상관이 없으니, 아무리 좋은 알고리즘을 써도 절대 잘 맞힐 수 없어요. **모델의 성능은 알고리즘보다 "데이터가 얼마나 문제와 관련 있는지"가 훨씬 중요하다**는 교훈이에요.

# ---

# ## 3. 중복 데이터 확인·제거 — Data Leakage 방지

# ```python
# iris[iris.duplicated(keep=False)]
# iris.iloc[:, :-1].duplicated(keep=False)   # target 빼고 확인
# iris.drop_duplicates(inplace=True)          # 중복 제거
# ```

# | 체크 방법 | 잡아내는 것 |
# |---|---|
# | `iris.duplicated()` (전체) | feature+target까지 완전히 똑같은 "진짜 중복" |
# | `iris.iloc[:, :-1].duplicated()` (target 제외) | 측정값은 같은데 정답만 다른 "데이터 오류 의심" |

# **왜 중복을 제거해야 하냐면 → "Data Leakage(데이터 누수)" 문제 때문이에요.**

# 같은 데이터가 학습용(train)이랑 시험용(test)에 둘 다 들어가 있으면, 모델이 "외운 걸 그대로 다시 보는 셈"이 돼서, 점수가 실제보다 훨씬 좋게 나와요. 근데 이건 진짜 실력이 아니라 **"답을 미리 알고 시험 본 것"**과 같아서, 실제 새로운 데이터에서는 성능이 뚝 떨어질 수 있어요. 그래서 중복을 미리 제거해서 이 문제를 막는 거예요.

# `inplace=True` → "원본을 직접 바꿔라"라는 뜻이에요 (새 변수에 담지 않고, `iris` 자체가 바뀜).

# ---

# ## 4. Train/Test 분리 (`train_test_split`)

# ```python
# X_train, X_test, y_train, y_test = train_test_split(
#     iris.iloc[:, :-1],   # X (features)
#     iris.target,          # y (정답)
#     test_size=0.1,        # 10%는 테스트용
#     stratify=iris.target, # 비율 유지!
# )
# ```

# | 변수 | 의미 |
# |---|---|
# | `X_train` | 학습용 features (90%) |
# | `X_test` | 시험용 features (10%) |
# | `y_train` | 학습용 정답 |
# | `y_test` | 시험용 정답 |

# ### `stratify`가 새로 나온 부분 — 이건 꼭 알아두세요

# **"target(정답)의 비율을 train/test에서 똑같이 유지해달라"**는 옵션이에요.

# 예를 들어 iris는 setosa/versicolor/virginica가 각각 50개씩 있는데, 그냥 랜덤하게 나누면 **운 나쁘면 test 세트에 setosa가 하나도 안 들어갈 수도 있어요.** `stratify=iris.target`을 쓰면, **train에도 test에도 세 품종이 원래 비율(각각 1/3씩)대로 골고루 섞이도록** 강제해줘요.

# **특히 데이터가 한쪽으로 치우친 경우(예: 정상 950개, 불량 50개)에 stratify를 꼭 써야 해요.** 안 그러면 test에 불량 데이터가 하나도 안 들어가서, "완벽하게 맞혔다"고 착각할 수 있거든요.

# ---

# ## 5. fit / predict / score 복습

# ```python
# lr = LogisticRegression()
# lr.fit(X_train, y_train)         # 학습 (X,y 둘 다 줌)
# lr.predict(X_test)                 # 예측 (X만 줌)
# lr.score(X_test, y_test)           # 채점 (X,y 둘 다 줌, 정답과 비교해서 점수 계산)
# ```

# - **fit** = 공부시키기
# - **predict** = 정답 없이 맞혀보기
# - **score** = predict + 정답 비교를 한 번에 (분류는 정확도, 회귀는 R²)
# ### 코드에 있던 재밌는 메모 하나

# ```python
# #! score 확률이 run할 때마다 달라지는데 그 이유 -> 데이터가 적어서
# ```

# **맞는 관찰이에요!** `train_test_split`은 기본적으로 **매번 랜덤하게** 데이터를 나눠요. 데이터가 적으면(iris는 150개뿐), 어쩌다 어려운 데이터가 test에 몰리느냐 쉬운 데이터가 몰리느냐에 따라 점수가 실행할 때마다 들쭉날쭉할 수 있어요.

# **이걸 고정하고 싶으면 `random_state`를 쓰면 돼요** (코드 뒷부분 breast_cancer 예시에서 `random_state=1`을 쓴 이유가 이거예요):

# ```python
# train_test_split(X, y, random_state=1)   # 항상 같은 방식으로 나눠짐 (재현 가능)
# ```

# ---

# ## 6. 결측치(NaN) 다루기 — 이 부분 꼭 이해하고 넘어가세요

# ### None vs NaN — 다른 거예요!

# ```python
# # ! float('nan') =! nan
# # print(mpg.loc[32].horsepower is None)
# ```

# - **`None`**: 파이썬의 "아무 값도 없다"는 표현
# - **`NaN`** (Not a Number): "숫자인데 값이 없다"는 표현. pandas/numpy가 결측치를 표시할 때 주로 씀
# **주의: NaN은 자기 자신과 비교해도 True가 안 나와요!**
# ```python
# float('nan') == float('nan')   # False!  (수학적으로 "정의되지 않음"이라 그럼)
# ```
# 그래서 결측치를 확인할 땐 `== NaN`이 아니라 `.isna()`, `.isnull()` 같은 전용 함수를 써야 해요.

# ### 결측치 확인하는 방법들

# ```python
# mpg.isnull()              # 각 칸마다 True/False로 결측치 여부 표시
# mpg.isna().any()          # 각 컬럼에 결측치가 하나라도 있는지
# mpg[mpg.horsepower.isna()] # 결측치가 있는 행만 보기 (불린 인덱싱!)
# mino.matrix(mpg)           # missingno로 그림으로 한눈에 보기
# ```

# ### 결측치를 채우는 방법

# ```python
# mpg.horsepower.fillna(0)   # NaN을 0으로 채우기
# ```

# ### 왜 리스트에 None을 넣으면 이상해지는지

# ```python
# b = np.array([None, 1, 2])
# # ! -> object로 인식된다. 숫자를 넣었는데도 -> 호모지니어스(동질성) 때문에
# # 그래서 NaN이라고 해서 넣는다.
# ```

# **numpy 배열은 "안에 있는 모든 원소가 같은 타입이어야 한다(homogeneous, 동질성)"는 규칙이 있어요.** `None`과 `1, 2`처럼 타입이 섞이면, numpy가 "그럼 이건 그냥 다 object(뭐든 담을 수 있는 타입)로 취급할게"라고 타협해버려요. 근데 이건 계산이 잘 안 되니까, 결측치 표현은 보통 `None`이 아니라 `NaN`(숫자 타입 안에서 "값 없음"을 표현하는 특별한 값)을 써요.

# ### 미리 처리하는 방법도 있음

# ```python
# #! 데이터 불러올 때마다 확인해서 바꿔야하나 ? -> read_csv() 에 받아올 때
# # 데이터를 미리 처리할 수 있다.
# ```

# `pd.read_csv()` 함수에 `na_values=`같은 옵션을 주면, 파일을 읽어올 때부터 특정 값을 결측치로 미리 지정할 수 있어요. 매번 나중에 손보지 않고 처음부터 깔끔하게 불러올 수 있는 거죠.

# ---

# ## 7. 인코딩 (문자를 숫자로 바꾸기) — 3가지 방법 비교

# | 방법 | 코드 | 결과 | 언제 쓰나 |
# |---|---|---|---|
# | **LabelEncoder** | `le.fit_transform(mpg.origin)` | 컬럼 1개, 0/1/2 숫자로 | **target(정답) 인코딩용** (모델이 순서로 착각해도 상관없는 경우) |
# | **OrdinalEncoder** | `oe.fit_transform(mpg.origin.values.reshape(-1,1))` | 컬럼 1개, 0/1/2 숫자로 | **feature 인코딩용**, 카테고리에 진짜 순서가 있을 때 |
# | **OneHotEncoder / get_dummies** | `pd.get_dummies(mpg["origin"])` | 카테고리 개수만큼 컬럼, 0/1로 | **feature 인코딩용**, 카테고리에 순서가 없을 때 (국가, 성별 등) |

# ### LabelEncoder vs OrdinalEncoder 차이 (둘이 비슷해 보이지만!)

# **`LabelEncoder`는 원래 y(target, 정답)를 인코딩하려고 만들어진 함수**예요. 그래서 1차원 배열을 그대로 받아요 (`le.fit_transform(mpg.origin)`, reshape 필요 없음).

# **`OrdinalEncoder`는 X(feature)를 인코딩하려고 만들어진 함수**예요. 그래서 scikit-learn의 다른 feature 처리 도구들처럼 2차원 입력이 필요해요 (`reshape(-1,1)` 필요).

# **실전 팁**: target을 인코딩할 땐 LabelEncoder, feature(순서 없는 카테고리)를 인코딩할 땐 OneHotEncoder(또는 get_dummies)를 쓰는 게 일반적이에요.

# ### `le.inverse_transform`도 나왔었죠

# ```python
# le.inverse_transform([0,1,2])
# ```
# 숫자로 인코딩했던 걸 **다시 원래 문자로 되돌리는** 기능이에요. 예측 결과가 숫자로 나올 때, "이 숫자가 원래 무슨 뜻이었지?"를 확인할 때 씀.

# ---

# ## 8. groupby — 그룹별로 계산하기 (titanic 예시)

# ```python
# titanic.groupby("sex")[["survived"]].sum() / len(titanic)
# ```

# 이건 **"성별(sex)로 그룹을 나누고, 각 그룹의 생존자(survived) 합을 구하기"**예요.

# ```python
# titanic.groupby("sex")             # 1. sex 기준으로 그룹 나누기 (male 그룹, female 그룹)
#        [["survived"]]              # 2. survived 컬럼만 보기
#        .sum()                      # 3. 그룹별로 합계 구하기 (생존자=1이니까 합계=생존자 수)
#        / len(titanic)              # 4. 전체 인원수로 나눠서 비율로 바꾸기
# ```

# **"성별에 따라 생존율이 어떻게 다른지"** 한 줄로 계산하는 코드예요. `value_counts()`가 "값 하나하나를 세는 것"이라면, `groupby`는 **"그룹으로 나눠서, 그룹마다 원하는 계산(합, 평균 등)을 하는 것"**이에요.

# ---

# ## 9. 스케일링 — StandardScaler

# ```python
# from sklearn.preprocessing import StandardScaler
# ss = StandardScaler()
# breast_std[["worst area"]] = ss.fit_transform(breast[["worst area"]])
# ```

# **"값의 범위(단위)가 큰 컬럼과 작은 컬럼이 섞여 있으면, 모델이 큰 숫자를 더 중요하다고 착각할 수 있어서, 평균 0·표준편차 1로 맞춰주는 전처리"**예요.

# - `fit`: 평균/표준편차 계산
# - `transform`: 계산한 값으로 실제 변환
# - `fit_transform`: 두 개를 한 번에
# **이 수업 코드의 마지막 실험**: `worst area` 컬럼 하나만 스케일링한 다음, 스케일링 전/후로 로지스틱 회귀 점수(`lr.score`, `lr_.score`)를 비교해봤어요. **스케일링이 모델 성능에 어떤 영향을 주는지 직접 확인해보려는 목적**이었어요.

# ---

# ## 10. 지금까지 배운 것 중 "특히 중요한" 핵심 개념 5가지

# 1. **데이터 나누기(Train/Test) + stratify** — 공정한 평가를 위해 필수. 데이터 비율이 안 맞으면 `stratify` 꼭 쓰기.
# 2. **중복 제거 = Data Leakage 방지** — 시험에 학습 데이터가 섞이면 점수를 믿을 수 없음.
# 3. **결측치는 `None`이 아니라 `NaN`으로, `.isna()`로 확인** — `== NaN` 비교는 항상 False라서 안 통함.
# 4. **범주형 데이터는 순서 유무에 따라 인코딩 방법이 다름** — 순서 있으면 Ordinal/Label, 순서 없으면 OneHot.
# 5. **스케일링은 컬럼 간 단위 차이를 없애서 모델을 더 공정하게 만듦** — StandardScaler(평균0,표준편차1) vs MinMaxScaler(0~1 사이).
# ---

# ## 부록: `iris.drop_duplicates(inplace=True)` 관련 참고

# `inplace=True`는 "새 변수에 담지 말고, 원본 자체를 바로 바꿔라"는 뜻이에요. 반대로 `inplace=False`(기본값)이면, 원본은 그대로 두고 **바뀐 결과를 새로 반환**만 해줘요. 그래서 `inplace=False`일 땐 꼭 변수에 담아야 해요:

# ```python
# iris = iris.drop_duplicates()          # 기본값(False), 새로 담아야 함
# iris.drop_duplicates(inplace=True)     # True, 원본이 바로 바뀜 (담을 필요 없음)
## 10. 지금까지 배운 것 중 "특히 중요한" 핵심 개념 5가지

# 1. **데이터 나누기(Train/Test) + stratify** — 공정한 평가를 위해 필수. 데이터 비율이 안 맞으면 `stratify` 꼭 쓰기.
# 2. **중복 제거 = Data Leakage 방지** — 시험에 학습 데이터가 섞이면 점수를 믿을 수 없음.
# 3. **결측치는 `None`이 아니라 `NaN`으로, `.isna()`로 확인** — `== NaN` 비교는 항상 False라서 안 통함.
# 4. **범주형 데이터는 순서 유무에 따라 인코딩 방법이 다름** — 순서 있으면 Ordinal/Label, 순서 없으면 OneHot.
# 5. **스케일링은 컬럼 간 단위 차이를 없애서 모델을 더 공정하게 만듦** — StandardScaler(평균0,표준편차1) vs MinMaxScaler(0~1 사이).
# ---

# ## 부록: `iris.drop_duplicates(inplace=True)` 관련 참고

# `inplace=True`는 "새 변수에 담지 말고, 원본 자체를 바로 바꿔라"는 뜻이에요. 반대로 `inplace=False`(기본값)이면, 원본은 그대로 두고 **바뀐 결과를 새로 반환**만 해줘요. 그래서 `inplace=False`일 땐 꼭 변수에 담아야 해요:

# ```python
# iris = iris.drop_duplicates()          # 기본값(False), 새로 담아야 함
# iris.drop_duplicates(inplace=True)     # True, 원본이 바로 바뀜 (담을 필요 없음)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
import tensorflow as tf

# MLPClassifier((20,4))

# 0-9 를 구분하고 싶다 (예측) -> ML 기반으로
(X_train, y_train), (X_test, y_test) = tf.keras.datasets.mnist.load_data()  # holdout
# print(X_train.shape) #(60000, 28, 28) 28 by 28 이 6만개

X_train.reshape(60000, 28 * 28)  # 2차원인 데이터가 6만개 있는 것
ff = tf.keras.layers.Flatten(
    "channels_last"
)  # 머신러닝은 1차원만 받으니까 / 비정형테이터를 정형화
# = ff = tf.keras.layers.Flatten("channels_last")(X_train)
# print(dir(ff))
# print(ff(X_train))
# shape=(60000, 784) -> shape=(60000, 784) 한 행에 784개의 원소로 되어있고 그게 60000행이 있다
# 합성함수
# ! (60000, 784) * (784,5) = 60000, 5
# ! (60000, 784) × (784, 5)
# !         ↑        ↑
# !    같아야 함 (784 = 784) ✓
# ! 가운데 숫자(784)가 사라지고, 바깥쪽 숫자(60000, 5)만 남아서 결과 모양이 됩
# ! 28 x 28 이미지를 넣으면 5개짜리 값이 나온다

# * 5개의 perceptron 이 있다
# * 퍼셉트론 5개를 만들고, 입력과 연결해서 가중치 기반 계산을 하도록 하는 것
# print(tf.keras.layers.Dense(5)(tf.keras.layers.Flatten("channels_last")(X_train)))
# ! Keras 레이어는 "만들어질 때"가 아니라 "처음 호출될 때" 가중치가 생긴다
# xx = tf.keras.layers.Dense(5)
# print(xx.weights)   # 호출 전
# xx((tf.keras.layers.Flatten("channels_last")(X_train)))   # 실제로 데이터를 흘려보냄 (호출)
# print(xx.weights)    # 호출 후


# wine 세 종류 와인 구분
from sklearn.datasets import load_wine

wine = load_wine(as_frame=True).frame
# wine 은 2차원 데이터 (1차원인 데이터가 여러개 있는 것)
# print(wine)
t = tf.keras.layers.Dense(16)
# ! target 은 라벨링
tt = tf.keras.layers.Dense(3)  # 왜 3개?
# print(wine["target"].unique()) # -> [0 1 2] 그래서 3종류라는 걸 알 수 있음
# print(tt(t(wine)))
# print(tf.keras.layers.Softmax()(tt(t(wine))))

# * 컴포지션을 하면 묶어진채로 명령을 내릴 수 있다.

# model = tf.keras.models.Sequential(
#     [
#         tf.keras.layers.Flatten(input_shape=(28, 28)),
#         tf.keras.layers.Dense(128, activation="relu"),
#         tf.keras.layers.Dropout(0.2),
#         tf.keras.layers.Dense(10, activation="softmax"),
#     ]
# )

model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(5, activation="relu", input_shape=(10,)),
        tf.keras.layers.Dense(2, activation="softmax"),
    ]
)
print(model.summary())
